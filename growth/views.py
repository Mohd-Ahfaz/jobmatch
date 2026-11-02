from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from accounts.utils import get_profile
from jobs.utils import my_skills

from .services import analyze_skill_gap_for_target_role


@login_required
def skill_gap(request):
    profile = get_profile(request.user)
    if not profile.is_setup():
        messages.warning(request, "Please set up your profile first to analyze your skill gaps.")
        return redirect("upload_resume" if not profile.resume_file else "profile")

    owned = my_skills(request.user)
    analysis = analyze_skill_gap_for_target_role(profile, owned)

    return render(request, "growth/skill_gap.html", {
        "tab": "gap",
        "profile": profile,
        "target_role": analysis["target_role"],
        "required_skills": analysis["required_skills"],
        "gaps": analysis["gaps"],
        "mastered": analysis["mastered"],
        "owned_count": analysis["owned_count"],
        "missing_count": analysis["missing_count"],
        "readiness_percent": analysis["readiness_percent"],
    })
