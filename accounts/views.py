from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import Job
from jobs.utils import my_skills, ranked_jobs
from tracker.models import Application
from tracker.utils import reminders_for

from .forms import ProfileForm, ResumeUploadForm, SignupForm
from .models import Skill, UserSkill
from .utils import fill_from_resume, get_profile, save_skills


def home(request):
    if request.user.is_authenticated:
        profile = get_profile(request.user)
        if not profile.is_setup():
            return redirect("upload_resume" if not profile.resume_file else "profile")
        return redirect("dashboard")
    return render(request, "home.html")


def signup(request):
    form = SignupForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user, backend="accounts.backends.EmailAuthBackend")
        messages.info(request, "Account created! Step 1: Upload your resume so we can scan your name, education, experience, and skills.")
        return redirect("upload_resume")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def upload_resume(request):
    profile = get_profile(request.user)
    form = ResumeUploadForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        profile.resume_file = form.cleaned_data["resume_file"]
        profile.save()
        scanned = fill_from_resume(profile)

        items_found = []
        if scanned.get("name"):
            items_found.append("Name")
        if scanned.get("education"):
            items_found.append("Education")
        if scanned.get("experience"):
            items_found.append("Experience")
        skill_count = len(scanned.get("skills", []))
        if skill_count:
            items_found.append(f"{skill_count} skill{'s' if skill_count != 1 else ''}")

        summary = ", ".join(items_found) if items_found else "profile details"
        messages.success(
            request,
            f"Resume scanned successfully! We extracted your {summary}. Please review and confirm your details in Step 2."
        )
        return redirect("profile")

    return render(request, "accounts/resume_upload.html", {
        "form": form,
        "profile": profile,
    })


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    if not profile.is_setup():
        messages.warning(request, "You must set up your profile first before you can access the dashboard.")
        return redirect("upload_resume" if not profile.resume_file else "profile")

    applications = {app.job_id: app for app in Application.objects.filter(user=request.user)}
    jobs = ranked_jobs(Job.objects.all(), my_skills(request.user))
    for job in jobs:
        job.application = applications.get(job.id)
    top_jobs = [job for job in jobs if job.scam["level"] != "High"][:5]
    stages = [
        (label, Application.objects.filter(user=request.user, status=key).count())
        for key, label in Application.STATUSES
    ]
    return render(request, "accounts/dashboard.html", {
        "profile": profile,
        "name": profile.full_name or "there",
        "top_jobs": top_jobs,
        "stages": stages,
        "reminders": reminders_for(request.user),
    })


@login_required
def profile(request):
    profile = get_profile(request.user)
    # Skills already on the user — either manually added or scanned from resume
    chosen = Skill.objects.filter(userskill__user=request.user)
    was_not_setup = not profile.is_setup()

    # Detect if user just came from Step 1 (resume was scanned and skills were added)
    scanned_skill_names = list(chosen.values_list("name", flat=True))

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile, initial={"skills": chosen})
        if form.is_valid():
            profile = form.save()
            save_skills(request.user, form.cleaned_data["skills"])

            if was_not_setup and profile.is_setup():
                messages.success(request, "🎉 Profile setup complete! Welcome to your dashboard.")
                return redirect("dashboard")
            else:
                messages.success(request, "Profile updated successfully.")
                return redirect("dashboard" if request.GET.get("next") == "dashboard" else "profile")
    else:
        form = ProfileForm(instance=profile, initial={"skills": chosen})

    return render(request, "accounts/profile.html", {
        "form": form,
        "profile": profile,
        "is_initial_setup": was_not_setup,
        "scanned_skill_names": scanned_skill_names,
    })


@login_required
def quiz_list(request):
    # Only show quizzes for skills the user has selected in their profile
    user_skill_ids = UserSkill.objects.filter(user=request.user).values_list("skill_id", flat=True)
    mine = {us.skill_id: us for us in UserSkill.objects.filter(user=request.user)}
    # Intersection: user's profile skills that also have quiz questions
    skills = Skill.objects.filter(
        id__in=user_skill_ids,
        questions__isnull=False
    ).distinct()
    rows = [(skill, mine.get(skill.id)) for skill in skills]
    # Count profile skills that have no quiz available yet
    no_quiz_count = len(user_skill_ids) - skills.count()
    return render(request, "accounts/quiz_list.html", {
        "rows": rows,
        "no_quiz_count": no_quiz_count,
    })


@login_required
def quiz_take(request, skill_id):
    skill = get_object_or_404(Skill, id=skill_id)
    # Block access if this skill is not in the user's profile
    if not UserSkill.objects.filter(user=request.user, skill=skill).exists():
        messages.warning(
            request,
            f"Add '{skill.name}' to your profile skills first before taking this quiz."
        )
        return redirect("quiz_list")
    questions = skill.questions.all()
    if not questions:
        return redirect("quiz_list")

    if request.method == "POST":
        score = sum(1 for q in questions if request.POST.get(f"q{q.id}") == q.correct)
        ratio = score / len(questions)
        level = "advanced" if ratio >= 0.9 else "intermediate" if ratio >= 0.6 else "beginner"
        UserSkill.objects.update_or_create(
            user=request.user, skill=skill,
            defaults={"level": level, "verified": ratio >= 0.6},
        )
        if ratio >= 0.6:
            messages.success(request, f"You scored {score}/{len(questions)} in {skill.name}. Level: {level}. Skill verified.")
        else:
            messages.info(request, f"You scored {score}/{len(questions)} in {skill.name}. Level: {level}. Score at least 60% to get verified.")
        return redirect("quiz_list")

    return render(request, "accounts/quiz.html", {"skill": skill, "questions": questions})
