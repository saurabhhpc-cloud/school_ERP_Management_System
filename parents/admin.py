from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from school_erp_ai.admin_site import admin_site
from .models import Parent


class ParentAdmin(admin.ModelAdmin):
    list_display = ("user", "emergency_contact", "occupation")


try:
    admin_site.register(Parent, ParentAdmin)
except AlreadyRegistered:
    pass

