from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile, UserSkill
from accounts.utils import get_profile
from tracker.models import Application

from .models import Job
from .services import fetch_remotive_jobs, fetch_muse_jobs, fetch_adzuna_jobs, suggest_jobs_with_gemini
from .utils import chance_score, match_info, my_skills, ranked_jobs, salary_estimate, scam_check


@login_required
def job_list(request):
    profile = get_profile(request.user)
    if not profile.is_setup():
        messages.warning(request, "Please set up your profile first to unlock your personalized job matches.")
        return redirect("upload_resume" if not profile.resume_file else "profile")

    jobs = Job.objects.all()
    get = request.GET

    if get.get("role"):
        jobs = jobs.filter(title__icontains=get["role"].strip())
    if get.get("location"):
        jobs = jobs.filter(location__icontains=get["location"].strip())
    if get.get("salary", "").isdigit():
        jobs = jobs.filter(max_salary__gte=int(get["salary"]))
    if get.get("level"):
        jobs = jobs.filter(level=get["level"])
    if get.get("work") == "remote":
        jobs = jobs.filter(is_remote=True)
    if get.get("work") == "onsite":
        jobs = jobs.filter(is_remote=False)
    if get.get("posted", "").isdigit():
        jobs = jobs.filter(posted_on__gte=date.today() - timedelta(days=int(get["posted"])))

    jobs = ranked_jobs(jobs, my_skills(request.user))

    # Attach existing application status to each job
    applications = {app.job_id: app for app in Application.objects.filter(user=request.user)}
    for job in jobs:
        job.application = applications.get(job.id)

    # Filter by minimum skill match percentage
    if get.get("min_match", "").isdigit():
        threshold = int(get["min_match"])
        jobs = [j for j in jobs if j.match["percent"] >= threshold]

    # Filter by application status
    if get.get("status") == "unapplied":
        jobs = [j for j in jobs if not j.application or j.application.status == "saved"]
    elif get.get("status") == "applied":
        jobs = [j for j in jobs if j.application and j.application.status != "saved"]

    return render(request, "jobs/job_list.html", {"jobs": jobs, "levels": Profile.LEVELS})


@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job.objects.prefetch_related("skills"), id=pk)
    owned = my_skills(request.user)
    match = match_info(job, owned)
    application = Application.objects.filter(user=request.user, job=job).first()
    return render(request, "jobs/job_detail.html", {
        "job": job,
        "match": match,
        "scam": scam_check(job),
        "estimate": salary_estimate(job),
        "chance": chance_score(job, match, owned, get_profile(request.user)),
        "application": application,
    })


@login_required
def suggest_real_jobs(request):
    """
    Fetch live, real tech jobs matching the logged-in user's skills
    from public job boards (Remotive, The Muse, Adzuna) and Gemini AI.
    """
    profile = get_profile(request.user)
    if not profile.is_setup():
        messages.warning(request, "Please complete your profile setup first.")
        return redirect("upload_resume" if not profile.resume_file else "profile")

    user_skills = list(UserSkill.objects.filter(user=request.user).values_list("skill__name", flat=True))
    if not user_skills:
        messages.warning(request, "Please select at least one skill in your profile so we can find matching jobs.")
        return redirect("profile")

    sources_found = {}

    # 1. Remotive (free, no key, remote jobs)
    for skill_name in user_skills[:3]:
        jobs = fetch_remotive_jobs(query=skill_name, limit=8)
        if jobs:
            sources_found["Remotive"] = sources_found.get("Remotive", 0) + len(jobs)

    # 2. The Muse (free, no key)
    muse_jobs = fetch_muse_jobs(user_skills, limit=10)
    if muse_jobs:
        sources_found["The Muse"] = len(muse_jobs)

    # 3. Adzuna (free tier, needs key — skips gracefully if not configured)
    adzuna_jobs = fetch_adzuna_jobs(user_skills, limit=10)
    if adzuna_jobs:
        sources_found["Adzuna"] = len(adzuna_jobs)

    # 4. Gemini AI suggestions (if key configured)
    gemini_jobs = suggest_jobs_with_gemini(
        skills_list=user_skills,
        target_role=profile.target_role or "Software Developer",
        location=profile.city or "Remote",
    )
    if gemini_jobs:
        sources_found["Gemini AI"] = len(gemini_jobs)

    top_skills_str = ", ".join(user_skills[:4])
    total = sum(sources_found.values())
    if total > 0:
        sources_str = ", ".join(f"{src} ({n})" for src, n in sources_found.items())
        messages.success(request, f"Found {total} real live jobs for your skills ({top_skills_str}) from: {sources_str}. Apply directly on each company's official portal.")
    else:
        messages.info(request, f"Live scan complete for skills: {top_skills_str}. Showing all matched jobs below.")

    return redirect("job_list")
