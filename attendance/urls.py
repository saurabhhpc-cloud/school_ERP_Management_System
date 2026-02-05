from django.urls import path
from . import views

app_name = "attendance" 
urlpatterns = [
    path("class-wise/", views.class_wise_attendance, name="class_wise"),
    path("percentage/", views.attendance_percentage, name="percentage"),
    path("summary/", views.today_summary, name="summary"),
    path("import/", views.import_attendance_excel, name="import"),
    path("overview/", views.attendance_overview, name="overview"),
    path("low-attendance/", views.low_attendance_alerts, name="low_attendance"),
    path("student-monthly/", views.student_monthly_attendance, name="student_monthly"),
    path("mark/", views.mark_attendance, name="mark"),
    path("attendance/mark/", views.mark_attendance, name="mark_attendance"),

]

