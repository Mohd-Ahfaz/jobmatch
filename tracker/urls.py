from django.urls import path
from . import views

urlpatterns = [
    path("", views.board, name="board"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("save/<int:job_id>/", views.save_job, name="save_job"),
    path("<int:pk>/", views.detail, name="application_detail"),
    path("<int:pk>/status/", views.change_status, name="change_status"),
    path("<int:pk>/update/", views.update_details, name="update_application_details"),
    path("<int:pk>/note/", views.add_note, name="add_application_note"),
    path("<int:pk>/documents/", views.documents, name="documents"),
    path("<int:pk>/interview/", views.interview, name="interview"),
    path("<int:pk>/delete/", views.delete, name="delete_application"),
]
