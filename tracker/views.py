from datetime import date
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.utils import get_profile
from jobs.models import Job
from jobs.services import generate_gemini_cover_letter
from jobs.utils import match_info, my_skills, scam_check

from .models import Application, ApplicationNote, InterviewAnswer
from .utils import (answer_feedback, ats_check, gmail_compose_link, interview_questions, mail_link,
                    make_cover_letter, make_resume, reminders_for)


def get_application(request, pk):
    return get_object_or_404(Application.objects.select_related("job"), id=pk, user=request.user)


@login_required
def board(request):
    profile = get_profile(request.user)
    if not profile.is_setup():
        messages.warning(request, "Please set up your profile first before accessing your application tracker.")
        return redirect("upload_resume" if not profile.resume_file else "profile")

    applications = Application.objects.filter(user=request.user).select_related("job").order_by("-applied_on", "-saved_on")
    columns = [
        (key, label, [app for app in applications if app.status == key])
        for key, label in Application.STATUSES
    ]
    return render(request, "tracker/board.html", {
        "columns": columns,
        "reminders": reminders_for(request.user),
        "total_count": applications.count(),
    })


@login_required
@require_POST
def save_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    application, created = Application.objects.get_or_create(user=request.user, job=job)
    if created:
        messages.success(request, f"{job.title} at {job.company} saved to your tracker.")
    return redirect("application_detail", pk=application.id)


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job.objects.prefetch_related("skills"), id=job_id)
    profile = get_profile(request.user)
    owned = my_skills(request.user)
    match = match_info(job, owned)
    scam = scam_check(job)
    application = Application.objects.filter(user=request.user, job=job).first()

    if request.method == "POST":
        resume_text = request.POST.get("resume_text", "").strip() or make_resume(request.user, profile, job)
        cover_letter = request.POST.get("cover_letter", "").strip() or make_cover_letter(request.user, profile, job)
        method = request.POST.get("application_method", "portal")
        conf_id = request.POST.get("confirmation_id", "").strip()
        portal_url = request.POST.get("portal_url", "").strip() or job.apply_link
        notes = request.POST.get("notes", "").strip()

        if not application:
            application = Application(user=request.user, job=job)

        application.resume_text = resume_text
        application.cover_letter = cover_letter
        application.application_method = method
        application.confirmation_id = conf_id
        application.portal_url = portal_url
        if notes:
            application.notes = notes
        application.set_status("applied")
        application.save()

        # Log creation in journal
        method_label = dict(Application.METHODS).get(method, method)
        note_text = f"Application submitted via {method_label}."
        if conf_id:
            note_text += f" Confirmation ID: {conf_id}."
        ApplicationNote.objects.create(application=application, text=note_text)

        messages.success(
            request,
            f"Logged your application for {job.title} at {job.company}! "
            f"Follow-up reminder scheduled for {application.follow_up_on.strftime('%d %b %Y')}."
        )
        return redirect("application_detail", pk=application.id)

    # GET: Prepare application review page
    if application and application.resume_text:
        resume = application.resume_text
    else:
        resume = make_resume(request.user, profile, job)

    if application and application.cover_letter:
        cover = application.cover_letter
    else:
        cover = generate_gemini_cover_letter(profile, job, match["have"]) or make_cover_letter(request.user, profile, job)
    ats = ats_check(resume, job)

    contact_target = job.contact_email or (application.recruiter_email if application else "")
    applicant_name = profile.full_name or request.user.username
    apply_subject = f"Application for {job.title} - {applicant_name}"
    apply_body = (
        f"{cover}\n\n"
        f"--- APPLICANT PROFILE SUMMARY ---\n"
        f"Candidate: {applicant_name}\n"
        f"Email: {request.user.email}\n"
        f"Location: {profile.city or 'Remote'}\n"
        f"Experience Level: {profile.get_experience_level_display()}\n\n"
        f"--- TAILORED RESUME ---\n"
        f"{resume}\n"
    )
    apply_gmail_link = gmail_compose_link(contact_target, apply_subject, apply_body) if contact_target else ""
    apply_mail_link = mail_link(contact_target, apply_subject, apply_body) if contact_target else ""

    return render(request, "tracker/apply.html", {
        "job": job,
        "profile": profile,
        "match": match,
        "scam": scam,
        "resume": resume,
        "cover": cover,
        "ats": ats,
        "application": application,
        "owned": owned,
        "methods": Application.METHODS,
        "contact_target": contact_target,
        "apply_gmail_link": apply_gmail_link,
        "apply_mail_link": apply_mail_link,
    })


@login_required
@require_POST
def change_status(request, pk):
    application = get_application(request, pk)
    status = request.POST.get("status")
    if status in dict(Application.STATUSES):
        old_status = application.get_status_display()
        application.set_status(status)
        new_status = application.get_status_display()
        ApplicationNote.objects.create(
            application=application,
            text=f"Status updated from {old_status} to {new_status}."
        )
        messages.success(request, f"Updated status to {new_status}.")
    if request.POST.get("from") == "detail":
        return redirect("application_detail", pk=pk)
    return redirect("board")


@login_required
@require_POST
def update_details(request, pk):
    application = get_application(request, pk)

    # Status update
    new_status = request.POST.get("status")
    if new_status and new_status in dict(Application.STATUSES) and new_status != application.status:
        application.set_status(new_status)

    # Method & Reference
    application.application_method = request.POST.get("application_method", application.application_method)
    application.confirmation_id = request.POST.get("confirmation_id", "").strip()
    application.portal_url = request.POST.get("portal_url", "").strip()

    # Recruiter contact
    application.recruiter_name = request.POST.get("recruiter_name", "").strip()
    application.recruiter_email = request.POST.get("recruiter_email", "").strip()

    # Dates
    applied_on_str = request.POST.get("applied_on")
    if applied_on_str:
        try:
            application.applied_on = date.fromisoformat(applied_on_str)
        except ValueError:
            pass

    follow_up_str = request.POST.get("follow_up_on")
    if follow_up_str:
        try:
            application.follow_up_on = date.fromisoformat(follow_up_str)
        except ValueError:
            pass
    elif "follow_up_on" in request.POST:
        application.follow_up_on = None

    # Interview details
    interview_round = request.POST.get("interview_round", "").strip()
    application.interview_round = interview_round
    interview_date_str = request.POST.get("interview_date", "").strip()
    if interview_date_str:
        try:
            application.interview_date = interview_date_str
        except Exception:
            pass

    # Offer details
    salary_str = request.POST.get("salary_offered", "").strip()
    if salary_str.isdigit():
        application.salary_offered = int(salary_str)
    elif "salary_offered" in request.POST:
        application.salary_offered = None

    deadline_str = request.POST.get("offer_deadline", "").strip()
    if deadline_str:
        try:
            application.offer_deadline = date.fromisoformat(deadline_str)
        except ValueError:
            pass

    # General notes
    application.notes = request.POST.get("notes", "").strip()
    application.save()

    messages.success(request, "Application tracking details updated successfully.")
    return redirect("application_detail", pk=pk)


@login_required
@require_POST
def add_note(request, pk):
    application = get_application(request, pk)
    note_text = request.POST.get("note_text", "").strip()
    if note_text:
        ApplicationNote.objects.create(application=application, text=note_text)
        messages.success(request, "Journal note saved.")
    return redirect("application_detail", pk=pk)


@login_required
@require_POST
def delete(request, pk):
    get_application(request, pk).delete()
    messages.success(request, "Removed application from your tracker.")
    return redirect("board")


@login_required
def detail(request, pk):
    application = get_application(request, pk)
    job = application.job
    profile = get_profile(request.user)
    name = profile.full_name or request.user.username

    contact_target = application.recruiter_email or job.contact_email

    follow_text = (
        f"Hi {application.recruiter_name or 'Hiring Team'},\n\n"
        f"I hope you are doing well. I wanted to follow up on my application for the {job.title} "
        f"role at {job.company}"
        + (f" (Application ID: {application.confirmation_id})" if application.confirmation_id else "") + ".\n\n"
        f"I remain enthusiastic about the opportunity and would appreciate any update on next steps.\n\n"
        f"Thank you for your time.\n\nBest regards,\n{name}\n{request.user.email}"
    )

    follow_subject = f"Following up: {job.title} - {name}"
    follow_mail = mail_link(contact_target, follow_subject, follow_text) if contact_target else ""
    gmail_link = gmail_compose_link(contact_target, follow_subject, follow_text) if contact_target else ""

    journal_notes = application.journal_notes.all()

    return render(request, "tracker/detail.html", {
        "app": application,
        "job": job,
        "scam": scam_check(job),
        "follow_text": follow_text,
        "follow_mail": follow_mail,
        "gmail_link": gmail_link,
        "contact_target": contact_target,
        "statuses": Application.STATUSES,
        "methods": Application.METHODS,
        "journal_notes": journal_notes,
    })


@login_required
def documents(request, pk):
    application = get_application(request, pk)
    profile = get_profile(request.user)

    if request.method == "POST":
        application.resume_text = request.POST.get("resume_text", "")
        application.cover_letter = request.POST.get("cover_letter", "")
        application.save()
        messages.success(request, "Tailored documents saved.")
        return redirect("documents", pk=pk)

    resume = application.resume_text or make_resume(request.user, profile, application.job)
    cover = application.cover_letter or make_cover_letter(request.user, profile, application.job)
    return render(request, "tracker/documents.html", {
        "app": application,
        "profile": profile,
        "resume": resume,
        "cover": cover,
        "ats": ats_check(resume, application.job),
    })


@login_required
def interview(request, pk):
    application = get_application(request, pk)
    questions = interview_questions(application.job)

    if request.method == "POST":
        index = request.POST.get("index", "")
        answer = request.POST.get("answer", "").strip()
        if index.isdigit() and int(index) < len(questions) and answer:
            question = questions[int(index)]
            feedback = answer_feedback(question, answer, application.job)
            InterviewAnswer.objects.update_or_create(
                application=application, question=question,
                defaults={"answer": answer, "feedback": feedback},
            )
            messages.success(request, "Answer evaluated! Review your feedback below.")
        return redirect("interview", pk=pk)

    saved = {item.question: item for item in application.answers.all()}
    items = [(i, question, saved.get(question)) for i, question in enumerate(questions)]
    return render(request, "tracker/interview.html", {"app": application, "items": items})
