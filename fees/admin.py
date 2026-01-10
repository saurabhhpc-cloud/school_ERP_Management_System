from django.contrib import admin
from .models import FeeStructure, StudentFee

@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ("class_name", "amount")
    search_fields = ("class_name",)


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display = ("student", "total_amount", "paid_amount", "status", "due_date")
    list_filter = ("status", "due_date")
    search_fields = ("student__full_name",)


# Register your models here.
