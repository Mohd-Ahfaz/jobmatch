import json
import re
import urllib.parse
import urllib.request
from datetime import date
from django.conf import settings
from accounts.models import Skill
from jobs.models import Job


def clean_html(raw_html):
    """Clean HTML tags and unescape entities into clean plain text."""
    if not raw_html:
        return ""
    text = re.sub(r"<br\s*/?>", "\n", raw_html, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<li[^>]*>", "• ", text, flags=re.IGNORECASE)
    text = re.sub(r"</li>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def find_matching_db_skills(text):
    """Find Skill objects whose names appear in the given text."""
    text_lower = text.lower()
    matched = []
    for skill in Skill.objects.all():
        name = skill.name
        # Match as whole word or boundary
        pattern = r"\b" + re.escape(name.lower()) + r"\b"
        if re.search(pattern, text_lower):
            matched.append(skill)
    return matched


def fetch_remotive_jobs(query=None, limit=15):
    """
    Fetch real live jobs from Remotive API (public, free, real company jobs).
    Matches and links jobs to skills in our database.
    """
    base_url = "https://remotive.com/api/remote-jobs"
    params = {}
    if query:
        params["search"] = str(query).strip()
    if limit:
        params["limit"] = limit

    url = base_url + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    saved_jobs = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            jobs_list = data.get("jobs", [])

            for item in jobs_list:
                apply_url = item.get("url", "").strip()
                if not apply_url:
                    continue

                # Check if already imported
                existing = Job.objects.filter(apply_link=apply_url).first()
                if existing:
                    saved_jobs.append(existing)
                    continue

                title = item.get("title", "Software Developer")[:150]
                company = item.get("company_name", "Tech Company")[:100]
                location = item.get("candidate_required_location", "Remote")[:100] or "Remote"
                desc = clean_html(item.get("description", ""))

                job = Job.objects.create(
                    title=title,
                    company=company,
                    location=location,
                    is_remote=True,
                    level="junior" if "junior" in title.lower() else "mid",
                    min_salary=8,
                    max_salary=16,
                    description=desc[:5000],
                    apply_link=apply_url,
                    contact_email="",
                    posted_on=date.today(),
                    is_real=True,
                    source="Remotive Live",
                )

                # Match skills from tags and title + description
                tags_text = " ".join(item.get("tags", [])) + " " + title + " " + desc[:1000]
                skills = find_matching_db_skills(tags_text)
                if skills:
                    job.skills.set(skills)

                saved_jobs.append(job)
    except Exception as e:
        print(f"[fetch_remotive_jobs] Error: {e}")

    return saved_jobs


def fetch_muse_jobs(skills_list, limit=10):
    """
    Fetch real jobs from The Muse API (free, no key needed).
    https://www.themuse.com/api/public/jobs
    """
    saved = []
    try:
        # Search for each top skill
        for skill in skills_list[:3]:
            url = "https://www.themuse.com/api/public/jobs?page=0&descending=true"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                results = data.get("results", [])
                for item in results[:limit]:
                    # Filter by skill match in name or contents
                    name = item.get("name", "")
                    contents = item.get("contents", "")
                    if skill.lower() not in name.lower() and skill.lower() not in contents.lower():
                        continue

                    apply_url = item.get("refs", {}).get("landing_page", "")
                    if not apply_url:
                        continue

                    existing = Job.objects.filter(apply_link=apply_url).first()
                    if existing:
                        saved.append(existing)
                        continue

                    company = ""
                    company_data = item.get("company", {})
                    if isinstance(company_data, dict):
                        company = company_data.get("name", "Tech Company")

                    locations = item.get("locations", [])
                    location = locations[0].get("name", "Remote") if locations else "Remote"

                    level_raw = item.get("levels", [{}])
                    level_name = level_raw[0].get("name", "Mid Level") if level_raw else "Mid Level"
                    level = "junior" if "junior" in level_name.lower() or "entry" in level_name.lower() else "mid"

                    desc = clean_html(contents)

                    job = Job.objects.create(
                        title=name[:150],
                        company=company[:100] or "Tech Company",
                        location=location[:100],
                        is_remote="remote" in location.lower() or not locations,
                        level=level,
                        min_salary=8, max_salary=20,
                        description=desc[:5000],
                        apply_link=apply_url[:500],
                        contact_email="",
                        posted_on=date.today(),
                        is_real=True,
                        source="The Muse",
                    )
                    matched_skills = find_matching_db_skills(name + " " + desc[:500])
                    if matched_skills:
                        job.skills.set(matched_skills)
                    saved.append(job)
    except Exception as e:
        print(f"[fetch_muse_jobs] Error: {e}")
    return saved


def fetch_adzuna_jobs(skills_list, limit=10):
    """
    Fetch real jobs from Adzuna API.
    Requires ADZUNA_APP_ID and ADZUNA_APP_KEY in settings/environment.
    Free tier: 250 calls/day. Register at https://developer.adzuna.com/
    """
    from django.conf import settings as django_settings
    app_id = getattr(django_settings, "ADZUNA_APP_ID", "") or ""
    app_key = getattr(django_settings, "ADZUNA_APP_KEY", "") or ""
    if not app_id or not app_key:
        return []  # Skip gracefully if keys not configured

    saved = []
    query = " OR ".join(skills_list[:3])
    url = (
        f"https://api.adzuna.com/v1/api/jobs/in/search/1"
        f"?app_id={app_id}&app_key={app_key}"
        f"&results_per_page={limit}&what={urllib.parse.quote(query)}&content-type=application/json"
    )
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            for item in data.get("results", []):
                apply_url = item.get("redirect_url", "")
                if not apply_url:
                    continue
                existing = Job.objects.filter(apply_link=apply_url).first()
                if existing:
                    saved.append(existing)
                    continue
                desc = clean_html(item.get("description", ""))
                job = Job.objects.create(
                    title=item.get("title", "Software Developer")[:150],
                    company=item.get("company", {}).get("display_name", "Company")[:100],
                    location=item.get("location", {}).get("display_name", "Remote")[:100],
                    is_remote=False,
                    level="junior",
                    min_salary=int(item.get("salary_min", 0) / 100000) or 5,
                    max_salary=int(item.get("salary_max", 0) / 100000) or 15,
                    description=desc[:5000],
                    apply_link=apply_url[:500],
                    contact_email="",
                    posted_on=date.today(),
                    is_real=True,
                    source="Adzuna",
                )
                matched_skills = find_matching_db_skills(item.get("title", "") + " " + desc[:500])
                if matched_skills:
                    job.skills.set(matched_skills)
                saved.append(job)
    except Exception as e:
        print(f"[fetch_adzuna_jobs] Error: {e}")
    return saved


def suggest_jobs_with_gemini(skills_list, target_role="Software Engineer", location="Remote"):
    """
    Call Gemini API to suggest real, verified hiring companies and live job postings
    tailored precisely to the user's skills and target role.
    """
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        return []

    skills_str = ", ".join(skills_list)
    prompt = f"""You are a tech career expert. Suggest 5 REAL, active or currently hiring tech jobs for a candidate with these skills: {skills_str}.
Target Role: {target_role}
Preferred Location: {location}

Return ONLY a valid JSON list of objects (no markdown code blocks, no other text). Each object must have:
- "title": Job title (e.g. "Junior Python Developer", "Frontend React Engineer")
- "company": Real tech company (e.g. "Canonical", "GitLab", "Automattic", "Red Hat", "Stripe", "Razorpay")
- "location": City or "Remote"
- "is_remote": boolean (true/false)
- "level": one of "fresher", "junior", "mid", "senior"
- "min_salary": integer annual salary in LPA (e.g. 5)
- "max_salary": integer annual salary in LPA (e.g. 10)
- "description": 2-3 paragraph job description with responsibilities and requirements
- "skills": list of skills needed (use standard names like Python, Django, React, SQL, Git, Docker, etc.)
- "apply_link": Real careers or application URL for this company (e.g. "https://canonical.com/careers" or "https://jobs.lever.co/company")
- "contact_email": careers email or ""
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json"}
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["candidates"][0]["content"]["parts"][0]["text"]
            # Clean possible markdown wrapping if any
            content = content.strip()
            if content.startswith("```"):
                content = re.sub(r"^```(?:json)?\s*", "", content)
                content = re.sub(r"\s*```$", "", content)

            suggested = json.loads(content)
            saved_jobs = []

            for item in suggested:
                apply_url = item.get("apply_link", "").strip() or f"https://www.google.com/search?q={urllib.parse.quote(item.get('company', '') + ' careers ' + item.get('title', ''))}"
                job, created = Job.objects.get_or_create(
                    title=item.get("title", "Software Developer")[:150],
                    company=item.get("company", "Tech Company")[:100],
                    defaults={
                        "location": item.get("location", location)[:100],
                        "is_remote": bool(item.get("is_remote", True)),
                        "level": item.get("level", "junior"),
                        "min_salary": item.get("min_salary", 6),
                        "max_salary": item.get("max_salary", 12),
                        "description": item.get("description", ""),
                        "apply_link": apply_url[:500],
                        "contact_email": item.get("contact_email", "")[:254],
                        "posted_on": date.today(),
                        "is_real": True,
                        "source": "Gemini AI Suggested",
                    }
                )

                # Link skill objects
                req_skills = item.get("skills", [])
                skill_objs = Skill.objects.filter(name__in=req_skills)
                if skill_objs.exists():
                    job.skills.set(skill_objs)
                else:
                    # Fallback auto match from text
                    auto_skills = find_matching_db_skills(item.get("title", "") + " " + item.get("description", ""))
                    if auto_skills:
                        job.skills.set(auto_skills)

                saved_jobs.append(job)
            return saved_jobs
    except Exception as e:
        print(f"[suggest_jobs_with_gemini] Error: {e}")
        return []


def generate_gemini_cover_letter(profile, job, matching_skills):
    """Generate a high-impact, personalized cover letter using Gemini if available."""
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if not api_key:
        return None

    skills_str = ", ".join(matching_skills) if matching_skills else "software development"
    prompt = f"""Write a professional, concise 3-paragraph cover letter for:
Candidate Name: {profile.full_name or 'Candidate'}
Candidate Skills: {skills_str}
Candidate Experience: {profile.experience or 'Hands-on projects and software development'}
Applying for: {job.title} at {job.company}
Job Description summary: {job.description[:400]}

Keep it polite, confident, highlighting specific skills, ready to send to a hiring manager. Do not use placeholders."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4}
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[generate_gemini_cover_letter] Error: {e}")
        return None
