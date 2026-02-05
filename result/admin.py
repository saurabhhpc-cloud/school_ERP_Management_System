from django.contrib import admin
from .models import Exam, Subject, Result
from django.contrib.admin.sites import AlreadyRegistered
from school_erp_ai.admin_site import admin_site
from django.utils.html import format_html


class ResultAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'exam',
        'subject',
        'marks_obtained',
    )
    list_filter = ('exam',)
    search_fields = ('student__name',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "subject":
            exam_id = request.GET.get('exam')
            if exam_id:
                try:
                    exam = Exam.objects.get(id=exam_id)
                    kwargs["queryset"] = Subject.objects.filter(
                        class_name=exam.class_name
                    )
                except Exam.DoesNotExist:
                    pass
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def status_badge(self, obj):
        if obj.status == 'PASS':
            return format_html(
                '<span style="color:green;font-weight:bold;">PASS</span>'
            )
        return format_html(
            '<span style="color:red;font-weight:bold;">FAIL</span>'
        )

    status_badge.short_description = "Status"

try:
    admin_site.register(Result, ResultAdmin)
except AlreadyRegistered:
    pass