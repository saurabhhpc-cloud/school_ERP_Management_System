from django.contrib import admin
from .models import Student

@admin.register(Student)

class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "student_id",
        "full_name",
        "class_name",
        "section",
        "gender",
        "parent_mobile",
        "created_at",
    )
    search_fields = ("full_name","student_id","parent_mobile")
    list_filter = ("class_name","section","gender")
# Register your models here.
