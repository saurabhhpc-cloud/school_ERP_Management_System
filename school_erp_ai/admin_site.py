from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin



class SchoolERPAdminSite(admin.AdminSite):
    site_header = "School ERP Dashboard"
    site_title = "School ERP Admin"
    index_title = "School ERP Dashboard"


admin_site = SchoolERPAdminSite(name="school_erp_admin")

# 🔥 REGISTER AUTH MODELS HERE (THIS WAS MISSING)
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

