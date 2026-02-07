from django.contrib import admin
from django import forms
from django.contrib.admin.sites import AlreadyRegistered

from school_erp_ai.admin_site import admin_site
from .models import Attendance
from admission.models import StudentProfile

class AttendanceAdminForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["student"].queryset = StudentProfile.objects.filter(
            is_active=True,
            roll_number__isnull=False,
            admission__admission_status="CONFIRMED"
        ).order_by("roll_number")

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm
    list_display = ("student", "date", "status", "teacher")
    list_filter = ("date", "status", "teacher")
    search_fields = (
        "student__first_name",
        "student__last_name",
        "student__roll_number",
    )

try:
    admin_site.register(Attendance, AttendanceAdmin)
except AlreadyRegistered:
    pass
