from django.contrib import admin
from school_erp_ai.admin_site import admin_site
from .models import Notice


class NoticeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "send_to_students",
        "send_to_teachers",
        "send_to_parents",
        "class_name",
        "publish_date",
        "is_active",
    )

    list_filter = (
        "send_to_students",
        "send_to_teachers",
        "send_to_parents",
        "is_active",
    )

    search_fields = ("title",)


admin_site.register(Notice, NoticeAdmin)
