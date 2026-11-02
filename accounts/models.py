from django.contrib.auth.models import User
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    LEVELS = [
        ("fresher", "Fresher"),
        ("junior", "Junior (1-3 years)"),
        ("mid", "Mid (3-6 years)"),
        ("senior", "Senior (6+ years)"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=True)
    education = models.CharField(max_length=200, blank=True)
    experience = models.TextField(blank=True)
    experience_level = models.CharField(max_length=10, choices=LEVELS, default="fresher")
    target_role = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    open_to_remote = models.BooleanField(default=True)
    expected_salary = models.PositiveIntegerField(null=True, blank=True)
    resume_file = models.FileField(upload_to="resumes/", blank=True)

    def __str__(self):
        return self.full_name or self.user.username

    def completeness(self):
        checks = [
            self.full_name,
            self.education,
            self.experience,
            self.target_role,
            self.city,
            self.expected_salary,
            self.resume_file,
            self.user.userskill_set.exists(),
        ]
        return int(sum(1 for item in checks if item) / len(checks) * 100)

    def is_setup(self):
        """Returns True if user has completed essential profile setup."""
        has_name = bool(self.full_name and self.full_name.strip())
        has_role = bool(self.target_role and self.target_role.strip())
        has_skills = self.user.userskill_set.exists() or bool(self.resume_file)
        return has_name and has_role and has_skills


class UserSkill(models.Model):
    LEVELS = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=15, choices=LEVELS, default="beginner")
    verified = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "skill")

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


class Question(models.Model):
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=300)
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.CharField(max_length=1, choices=[("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")])

    def __str__(self):
        return self.text

    def options(self):
        return [("a", self.option_a), ("b", self.option_b), ("c", self.option_c), ("d", self.option_d)]


from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
