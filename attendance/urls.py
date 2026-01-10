from django.urls import path
from .views import class_wise_attendance, attendance_percentage, today_summary

urlpatterns = [
    path("class-wise/", class_wise_attendance, name="class_wise_attendance"),
     path("percentage/", attendance_percentage, name="attendance_percentage"),
    path("summary/", today_summary, name="today_summary"),
]