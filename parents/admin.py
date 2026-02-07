from django.contrib import admin
from school_erp_ai.admin_site import admin_site
from .models import Parent


class ParentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
    )
    search_fields = ("user__username",)


admin_site.register(Parent, ParentAdmin)

