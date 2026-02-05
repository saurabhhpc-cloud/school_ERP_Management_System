from django.contrib.auth.admin import UserAdmin
from school_erp_ai.admin_site import admin_site
from accounts.models import User


class CustomUserAdmin(UserAdmin):

    
    fieldsets = UserAdmin.fieldsets + (
        ("School Info", {
            "fields": ("school",),
        }),
        ("Roles", {
            "fields": ("is_admin", "is_teacher", "is_parent"),
        }),
    )

    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("School Info", {
            "fields": ("school",),
        }),
        ("Roles", {
            "fields": ("is_admin", "is_teacher", "is_parent"),
        }),
    )

    list_display = ("username", "role", "is_active")
    list_filter = ("is_admin", "is_teacher", "is_parent")


admin_site.register(User, CustomUserAdmin)
