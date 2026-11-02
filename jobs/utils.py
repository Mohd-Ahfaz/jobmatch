from accounts.models import UserSkill

FREE_EMAIL_DOMAINS = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com"]
MONEY_WORDS = ["registration fee", "security deposit", "processing fee", "pay a fee", "deposit"]
PROMISE_WORDS = ["no interview", "immediate joining", "guaranteed", "100% placement"]
BASE_SALARY = {"fresher": 3, "junior": 5, "mid": 10, "senior": 18}


def my_skills(user):
    """Returns the user's skills as {skill name: UserSkill}."""
    return {us.skill.name: us for us in UserSkill.objects.filter(user=user).select_related("skill")}


def match_info(job, owned):
    required = [skill.name for skill in job.skills.all()]
    have = [name for name in required if name in owned]
    missing = [name for name in required if name not in owned]
    percent = round(len(have) / len(required) * 100) if required else 0
    return {"percent": percent, "have": have, "missing": missing, "total": len(required)}


def scam_check(job):
    points = 0
    reasons = []
    text = job.description.lower()
    domain = job.contact_email.split("@")[-1].lower() if job.contact_email else ""

    if domain in FREE_EMAIL_DOMAINS:
        points += 1
        reasons.append(f"The recruiter uses a free email address ({domain})")
    if any(word in text for word in MONEY_WORDS):
        points += 3
        reasons.append("The job asks you to pay a fee or deposit")
    if any(word in text for word in PROMISE_WORDS):
        points += 2
        reasons.append("The job makes promises that sound too good to be true")
    if len(job.description) < 120:
        points += 1
        reasons.append("The job duties are vague")
    if job.level == "fresher" and job.max_salary and job.max_salary > 20:
        points += 2
        reasons.append("The salary is very high for a fresher")

    level = "High" if points >= 3 else "Medium" if points >= 1 else "Low"
    return {"level": level, "reasons": reasons}


def salary_estimate(job):
    return round(BASE_SALARY[job.level] + job.skills.count() * 0.5, 1)


def chance_score(job, info, owned, profile):
    score = info["percent"] * 0.7
    if info["have"]:
        verified = [name for name in info["have"] if owned[name].verified]
        score += len(verified) / len(info["have"]) * 15
    if profile.experience_level == job.level:
        score += 15
    return max(5, min(95, round(score)))


def ranked_jobs(queryset, owned):
    """Returns jobs with .match and .scam attached, best match first."""
    jobs = list(queryset.prefetch_related("skills"))
    for job in jobs:
        job.match = match_info(job, owned)
        job.scam = scam_check(job)
    # risky jobs go to the bottom, then best match first
    return sorted(jobs, key=lambda job: (job.scam["level"] == "High", -job.match["percent"]))


def count_matches(jobs, skill_names, cutoff=60):
    count = 0
    for job in jobs:
        required = [skill.name for skill in job.skills.all()]
        if required and len([n for n in required if n in skill_names]) / len(required) * 100 >= cutoff:
            count += 1
    return count
