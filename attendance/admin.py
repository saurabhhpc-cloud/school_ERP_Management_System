from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from django import forms

from school_erp_ai.admin_site import admin_site
from .models import Attendance, AttendanceSummary
from students.models import Student


# ===============================
# Admin Form
# ===============================
class AttendanceAdminForm(forms.ModelForm):

    class Meta:
        model = Attendance
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Default empty
        self.fields["student"].queryset = Student.objects.none()

        # Filter students by class_name (from POST data)
        if "class_name" in self.data:
            try:
                class_id = int(self.data.get("class_name"))
                self.fields["student"].queryset = Student.objects.filter(
                    class_name_id=class_id
                )
            except (ValueError, TypeError):
                pass

        # Edit case
        elif self.instance.pk:
            self.fields["student"].queryset = Student.objects.filter(
                class_name=self.instance.student.class_name
            )


# ===============================
# Admin Model
# ===============================
class AttendanceAdmin(admin.ModelAdmin):
    form = AttendanceAdminForm

    list_display = ("student", "date", "is_present")
    list_filter = ("date", "is_present")
    search_fields = ("student__name",)


# ===============================
# SAFE REGISTER
# ===============================
try:
    admin_site.register(Attendance, AttendanceAdmin)
except AlreadyRegistered:
    pass
class AttendanceSummaryAdmin(admin.ModelAdmin):
    list_display = ("school", "month", "percentage")
    list_filter = ("school", "month")


try:
    admin_site.register(AttendanceSummary, AttendanceSummaryAdmin)
except AlreadyRegistered:
    pass