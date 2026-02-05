from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from school_erp_ai.admin_site import admin_site
from teacher.models import Teacher

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_active")
    list_filter = ("is_parent", "is_teacher", "is_admin")

    fieldsets = UserAdmin.fieldsets + (
        ("School Info", {
            "fields": ("school",),   # ✅ THIS WAS MISSING
        }),
        ("User Role", {
            "fields": ("is_parent", "is_teacher", "is_admin"),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("School Info", {
            "fields": ("school",),
        }),
        ("User Role", {
            "fields": ("is_parent", "is_teacher", "is_admin"),
        }),
    )
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if obj.is_teacher:
            Teacher.objects.get_or_create(
                user=obj,
                defaults={
                    "class_name": "",
                    "section": "",
                }
            )

admin_site.register(User, CustomUserAdmin)
