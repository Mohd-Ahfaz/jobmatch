from django.urls import path

from . import views

urlpatterns = [
    path("", views.skill_gap, name="skill_gap"),
]
