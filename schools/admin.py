from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from school_erp_ai.admin_site import admin_site
from .models import School


class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "board", "city", "state")



try:
    admin_site.register(School, SchoolAdmin)
except AlreadyRegistered:
    pass
