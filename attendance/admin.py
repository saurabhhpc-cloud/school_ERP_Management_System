from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student","date","status")
    list_filter = ("date","status")
    search_fields = ("student_full_name",)
# Register your models here.
