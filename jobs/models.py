from datetime import date

from django.db import models

from accounts.models import Profile, Skill


class Job(models.Model):
    title = models.CharField(max_length=150)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    level = models.CharField(max_length=10, choices=Profile.LEVELS, default="fresher")
    min_salary = models.PositiveIntegerField(null=True, blank=True)
    max_salary = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField()
    skills = models.ManyToManyField(Skill, blank=True)
    apply_link = models.URLField(max_length=500, blank=True)
    contact_email = models.EmailField(blank=True)
    posted_on = models.DateField(default=date.today)
    is_real = models.BooleanField(default=True)
    source = models.CharField(max_length=50, blank=True, default="Verified Career Portal")

    class Meta:
        ordering = ["-posted_on"]

    def __str__(self):
        return f"{self.title} at {self.company}"

    def salary_text(self):
        if self.min_salary and self.max_salary:
            return f"{self.min_salary}-{self.max_salary} LPA"
        return "Salary not listed"
