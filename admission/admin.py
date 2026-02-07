from django.contrib import admin
from school_erp_ai.admin_site import admin_site
from .models import *
from .models import StudentProfile, Admission, ParentProfile
from django.contrib.admin.sites import AlreadyRegistered

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "school",
        "roll_number",
        "is_active",
    )
    list_filter = ("school", "is_active")
    search_fields = ("first_name", "last_name", "roll_number")


@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "academic_year",
        "class_applied",
        "section",
        "admission_status",
    )
    list_filter = ("academic_year", "admission_status")
    search_fields = ("student__first_name", "student__last_name")


@admin.register(ParentProfile)
class ParentProfileAdmin(admin.ModelAdmin):
    list_display = ("father_name", "primary_mobile")



try:
    admin_site.register(StudentProfile, StudentProfileAdmin)
except AlreadyRegistered:
    pass

try:
    admin_site.register(Admission, AdmissionAdmin)
except AlreadyRegistered:
    pass

try:
    admin_site.register(ParentProfile, ParentProfileAdmin)
except AlreadyRegistered:
    pass


# Register your models here.
