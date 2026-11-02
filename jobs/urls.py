from django.urls import path

from . import views

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("suggest-real/", views.suggest_real_jobs, name="suggest_real_jobs"),
    path("<int:pk>/", views.job_detail, name="job_detail"),
]
