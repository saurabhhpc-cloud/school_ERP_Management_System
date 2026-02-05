from django.urls import path
from . import views

app_name = "teachers"

urlpatterns = [
    path("dashboard/", views.teacher_dashboard, name="dashboard"),
    path("", views.teacher_list, name="list"),   # ✅ ADD THIS
    path("attendance/", views.teacher_attendance, name="attendance"),
    path("attendance/mark/", views.mark_attendance, name="mark_attendance"),
    path("edit/<int:pk>/", views.teacher_edit, name="edit"),
    path("delete/<int:pk>/", views.teacher_delete, name="delete"),
]
