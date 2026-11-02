from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import Profile, Skill

from django.contrib.auth.models import User
from growth.roadmaps import ROLE_SKILL_ROADMAPS

# Build sorted choices for the target role dropdown
_TARGET_ROLE_CHOICES = [("", "— Select your target role —")] + [
    (role, role.title()) for role in sorted(ROLE_SKILL_ROADMAPS.keys())
]


class SignupForm(UserCreationForm):
    username = forms.EmailField(
        label="Email Address",
        help_text="Enter your real email address. You will use this to log in and apply for real jobs.",
        widget=forms.EmailInput(attrs={"placeholder": "e.g. yourname@gmail.com", "autocomplete": "off"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("password1", "password2"):
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    "autocomplete": "off",
                    "readonly": True,
                    "onfocus": "this.removeAttribute('readonly');",
                    "onpointerdown": "this.removeAttribute('readonly');",
                })

    def clean_username(self):
        email = self.cleaned_data.get("username", "").strip().lower()
        # Reject emails where the local part (before @) contains no letters at all
        local_part = email.split("@")[0] if "@" in email else email
        if local_part and not any(c.isalpha() for c in local_part):
            raise forms.ValidationError("Please enter a valid email address.")
        if User.objects.filter(email__iexact=email).exists() or User.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("An account with this email address already exists. Please log in.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data["username"].strip().lower()
        user.username = email
        user.email = email
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"placeholder": "e.g. yourname@gmail.com", "autocomplete": "off"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "password" in self.fields:
            self.fields["password"].widget.attrs.update({
                "autocomplete": "off",
                "readonly": True,
                "onfocus": "this.removeAttribute('readonly');",
                "onpointerdown": "this.removeAttribute('readonly');",
            })


class ResumeUploadForm(forms.Form):
    ALLOWED_EXTENSIONS = (".pdf", ".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tiff", ".tif")

    resume_file = forms.FileField(
        label="Select your PDF Resume",
        widget=forms.FileInput(attrs={
            "accept": ".pdf,.png,.jpg,.jpeg,.webp,.bmp,.tiff,.tif,image/*,application/pdf",
            "class": "form-control form-control-lg",
        }),
    )

    def clean_resume_file(self):
        file = self.cleaned_data.get("resume_file")
        if not file:
            raise forms.ValidationError("Please choose a resume file to upload.")
        name_lower = file.name.lower()
        if not any(name_lower.endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            raise forms.ValidationError("Unsupported file format. Please upload a PDF or image file (PDF, PNG, JPG, JPEG, WEBP).")
        if file.size > 15 * 1024 * 1024:
            raise forms.ValidationError("The resume file is too large (max 15MB).")
        return file


class ProfileForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name",
        widget=forms.TextInput(attrs={"placeholder": "e.g. Alex Morgan"}),
    )
    target_role = forms.ChoiceField(
        choices=_TARGET_ROLE_CHOICES,
        required=True,
        label="Target Job Role",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    education = forms.CharField(
        max_length=200,
        required=False,
        label="Education / Degree",
        widget=forms.TextInput(attrs={"placeholder": "e.g. B.Tech Computer Science"}),
    )
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    field_order = [
        "full_name", "target_role", "education", "experience", "experience_level",
        "city", "open_to_remote", "expected_salary", "skills",
    ]

    class Meta:
        model = Profile
        fields = [
            "full_name", "target_role", "education", "experience", "experience_level",
            "city", "open_to_remote", "expected_salary",
        ]
        labels = {
            "expected_salary": "Expected salary (LPA)",
            "open_to_remote": "Open to remote jobs",
            "experience_level": "Experience level",
        }
        widgets = {
            "experience": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Summary of your work experience, projects, and internships..."
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        skills = cleaned_data.get("skills")
        user = getattr(self.instance, "user", None)
        has_existing = user and user.userskill_set.exists() if user else False
        has_resume = self.instance and bool(self.instance.resume_file)
        if not skills and not has_existing and not has_resume:
            raise forms.ValidationError(
                "Please select at least one skill so we can match you with jobs."
            )
        return cleaned_data
