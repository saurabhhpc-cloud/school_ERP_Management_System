from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "institute", "city", "created_at")
    search_fields = ("name", "phone", "institute")


# Register your models here.
