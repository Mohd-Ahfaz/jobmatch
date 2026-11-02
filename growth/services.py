import re
from collections import Counter
from django.conf import settings
from accounts.models import Skill
from jobs.models import Job
from .roadmaps import ROLE_SKILL_ROADMAPS
from .utils import course_for


def get_target_role_skills(target_role):
    """
    Given a target role name, return the top 10 core skills required for that role.
    Uses:
    1. Direct match or fuzzy match in curated industry roadmaps.
    2. Real jobs in the database matching the target role keywords.
    3. Gemini AI suggestions if configured.
    4. Fallback to market top skills.
    """
    if not target_role:
        return []

    role_clean = target_role.strip().lower()

    # 1. Exact match in roadmaps
    if role_clean in ROLE_SKILL_ROADMAPS:
        return ROLE_SKILL_ROADMAPS[role_clean][:10]

    # 2. Substring / fuzzy match in roadmaps
    for key, skills in ROLE_SKILL_ROADMAPS.items():
        if key in role_clean or role_clean in key:
            return skills[:10]

    # 3. Check keywords (e.g. 'data', 'python', 'react', 'machine learning')
    for word in role_clean.split():
        if len(word) > 3:
            for key, skills in ROLE_SKILL_ROADMAPS.items():
                if word in key:
                    return skills[:10]

    # 4. Extract from real database jobs matching role
    matching_jobs = Job.objects.filter(title__icontains=target_role).prefetch_related("skills")
    if not matching_jobs.exists():
        # Try individual words
        for word in role_clean.split():
            if len(word) > 3:
                matching_jobs = Job.objects.filter(title__icontains=word).prefetch_related("skills")
                if matching_jobs.exists():
                    break

    if matching_jobs.exists():
        counts = Counter(skill.name for j in matching_jobs for skill in j.skills.all())
        if counts:
            return [name for name, _ in counts.most_common(10)]

    # 5. Gemini AI fallback if GEMINI_API_KEY is configured
    api_key = getattr(settings, "GEMINI_API_KEY", "")
    if api_key:
        try:
            import json
            import urllib.request
            prompt = f"List exactly 10 must-have technical skills for the role '{target_role}'. Return ONLY a JSON array of 10 skill strings."
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                parsed = json.loads(text)
                if isinstance(parsed, list) and len(parsed) >= 5:
                    return parsed[:10]
        except Exception:
            pass

    # 6. Default standard software engineering skills
    return ROLE_SKILL_ROADMAPS["software engineer"][:10]


def analyze_skill_gap_for_target_role(profile, owned_skills):
    """
    Analyzes the candidate's skills against their target role.
    Returns:
    - target_role: string
    - required_skills: list of 10 skills
    - owned_count: number of skills the user already has
    - readiness_percent: percentage (e.g. 60%)
    - gaps: list of tuples for missing skills (skill_name, course_title, course_url)
    - mastered: list of tuples for owned skills (skill_name, course_title, course_url)
    """
    target_role = profile.target_role or "Software Engineer"
    required_10 = get_target_role_skills(target_role)

    # Ensure list is at most 10 skills
    required_10 = required_10[:10]

    owned_set = set(owned_skills)

    gaps = []
    mastered = []

    for skill_name in required_10:
        course_title, course_url = course_for(skill_name)
        if skill_name in owned_set:
            mastered.append({
                "name": skill_name,
                "course_title": course_title,
                "course_url": course_url,
                "has_skill": True,
            })
        else:
            gaps.append({
                "name": skill_name,
                "course_title": course_title,
                "course_url": course_url,
                "has_skill": False,
            })

    total = len(required_10) or 10
    owned_count = len(mastered)
    readiness_percent = round((owned_count / total) * 100)

    return {
        "target_role": target_role,
        "required_skills": required_10,
        "gaps": gaps,
        "mastered": mastered,
        "owned_count": owned_count,
        "missing_count": len(gaps),
        "readiness_percent": readiness_percent,
    }
