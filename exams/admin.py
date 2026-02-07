from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from school_erp_ai.admin_site import admin_site
from .models import Exam, Subject, Result
from school_erp_ai.admin_mixins import SchoolScopedAdmin
from admission.models import StudentProfile

class ResultInline(admin.TabularInline):
    model = Result
    extra = 1

class ExamAdmin(SchoolScopedAdmin, admin.ModelAdmin):
    list_display = ("name", "class_name", "start_date", "end_date", "is_active")
    list_filter = ("class_name", "is_active")
    search_fields = ("name",)
    ordering = ("-start_date",)

class SubjectAdmin(SchoolScopedAdmin, admin.ModelAdmin):
    list_display = ("name", "class_name")
    list_filter = ("class_name",)
    search_fields = ("name",)


class ResultAdmin(SchoolScopedAdmin, admin.ModelAdmin):
    list_display = ("student", "exam", "subject", "marks_obtained")
    list_filter = ("exam",)
    search_fields = ("student__name",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # superuser ko sab dikhe
        if request.user.is_superuser:
            return super().formfield_for_foreignkey(db_field, request, **kwargs)

        # normal user → sirf apna school
        school = getattr(getattr(request.user, "userprofile", None), "school", None)
        if school:
            if db_field.name == "student":
                kwargs["queryset"] = StudentProfile.objects.filter(school=school)
            elif db_field.name == "exam":
                kwargs["queryset"] = Exam.objects.filter(school=school)
            elif db_field.name == "subject":
                kwargs["queryset"] = Subject.objects.filter(school=school)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


try:
    admin_site.register(Exam, ExamAdmin)
except AlreadyRegistered:
    pass

try:
    admin_site.register(Subject, SubjectAdmin)
except AlreadyRegistered:
    pass

try:
    admin_site.register(Result, ResultAdmin)
except AlreadyRegistered:
    pass