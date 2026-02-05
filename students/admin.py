from django.contrib import admin
from school_erp_ai.admin_site import admin_site
from .models import Student
from classrooms.models import ClassRoom


class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "class_name")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "class_name":
            if request.user.is_superuser:
                kwargs["queryset"] = ClassRoom.objects.all()
            else:
                kwargs["queryset"] = ClassRoom.objects.filter(
                    school=request.user.school
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 🔥 IMPORTANT: register with custom admin_site
admin_site.register(Student, StudentAdmin)

