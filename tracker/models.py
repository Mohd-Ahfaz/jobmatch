from datetime import date, timedelta
from django.contrib.auth.models import User
from django.db import models
from jobs.models import Job


class Application(models.Model):
    STATUSES = [
        ("saved", "Saved"),
        ("applied", "Applied"),
        ("interview", "Interview"),
        ("offer", "Offer"),
        ("rejected", "Rejected"),
    ]

    METHODS = [
        ("portal", "Company Portal (Workday, Greenhouse, Lever, etc.)"),
        ("linkedin", "LinkedIn Easy Apply / Job Post"),
        ("referral", "Employee Referral"),
        ("email", "Direct Email to Recruiter"),
        ("other", "Other Job Board / Career Fair"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUSES, default="saved")
    application_method = models.CharField(max_length=20, choices=METHODS, default="portal")
    confirmation_id = models.CharField(max_length=100, blank=True, help_text="Requisition or Confirmation #")
    recruiter_name = models.CharField(max_length=100, blank=True)
    recruiter_email = models.EmailField(blank=True)
    portal_url = models.URLField(max_length=500, blank=True)
    saved_on = models.DateField(auto_now_add=True)
    applied_on = models.DateField(null=True, blank=True)
    replied_on = models.DateField(null=True, blank=True)
    follow_up_on = models.DateField(null=True, blank=True)
    interview_date = models.DateTimeField(null=True, blank=True)
    interview_round = models.CharField(max_length=100, blank=True)
    salary_offered = models.PositiveIntegerField(null=True, blank=True, help_text="Offered Salary (LPA)")
    offer_deadline = models.DateField(null=True, blank=True)
    resume_text = models.TextField(blank=True)
    cover_letter = models.TextField(blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("user", "job")

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"

    def set_status(self, new_status):
        if new_status == "applied" and not self.applied_on:
            self.applied_on = date.today()
            if not self.follow_up_on:
                self.follow_up_on = date.today() + timedelta(days=7)
        if new_status in ("interview", "offer", "rejected") and not self.replied_on:
            self.replied_on = date.today()
        self.status = new_status
        self.save()

    def days_since_applied(self):
        if self.applied_on:
            return (date.today() - self.applied_on).days
        return None


class ApplicationNote(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="journal_notes")
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note on {self.application.job.title} ({self.created_at.strftime('%d %b %Y')})"


class InterviewAnswer(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name="answers")
    question = models.CharField(max_length=300)
    answer = models.TextField()
    feedback = models.TextField()
