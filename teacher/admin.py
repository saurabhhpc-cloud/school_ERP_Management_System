from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import Teacher
from school_erp_ai.admin_site import admin_site


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("user", "class_name", "section")


# ✅ SAFE REGISTRATION
try:
    admin_site.register(Teacher, TeacherAdmin)
except AlreadyRegistered:
    pass

