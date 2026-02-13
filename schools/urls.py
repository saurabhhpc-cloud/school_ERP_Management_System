from django.urls import path
from . import views

app_name = "schools"

urlpatterns = [
    path("dashboard/", views.school_dashboard, name="dashboard"),

    path("today-attendance/", views.today_attendance, name="today-attendance"),

    path("export/attendance/excel/", views.export_attendance_excel, name="export-attendance-excel"),
    path("export/attendance/pdf/", views.export_attendance_pdf, name="export-attendance-pdf"),

    path("export/fees/excel/", views.export_fees_excel, name="export-fees-excel"),
    path("export/fees/pdf/", views.export_fees_pdf, name="export-fees-pdf"),

    path("principal/dashboard/", views.principal_dashboard, name="principal-dashboard"),
    path("principal/class/<str:class_name>/sections/", views.principal_class_sections, name="principal-class-sections"),
]