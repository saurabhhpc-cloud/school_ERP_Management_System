from django.contrib import admin
from django.contrib.admin.sites import AlreadyRegistered
from .models import FeeStructure, FeePayment
from school_erp_ai.admin_site import admin_site


class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ("class_name", "fee_type", "amount")


class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ("student", "amount_paid", "status", "created_at")
    list_filter = ("status", "payment_mode", "created_at")


# ✅ SAFE REGISTRATION
try:
    admin_site.register(FeeStructure, FeeStructureAdmin)
except AlreadyRegistered:
    pass

try:
    admin_site.register(FeePayment, FeePaymentAdmin)
except AlreadyRegistered:
    pass

