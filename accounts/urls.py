from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),
    path("accounts/login/", auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("profile/upload-resume/", views.upload_resume, name="upload_resume"),
    path("profile/", views.profile, name="profile"),
    path("skills/", views.quiz_list, name="quiz_list"),
    path("skills/<int:skill_id>/quiz/", views.quiz_take, name="quiz_take"),
]
