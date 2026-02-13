from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    path("", views.students_list, name="students_list"),
    path("add/", views.add_student, name="add_student"),
    path("edit/<int:student_id>/", views.edit_student, name="edit_student"),
    path("toggle-status/<int:student_id>/",
     views.toggle_status,
     name="toggle_status"),
    path("report/<int:student_id>/", views.student_report, name="report"),
    path("import/", views.import_students_excel, name="import_students"),
    path("ajax-filter/", views.ajax_filter_students, name="ajax_filter"),
]
