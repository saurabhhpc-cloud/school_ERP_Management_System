# fees/views.py
from django.shortcuts import render, get_object_or_404
from django.db.models import Sum
from .models import FeePayment
from admission.models import StudentProfile

from django.http import HttpResponse


def defaulters_report(request):
    return HttpResponse("Defaulters Report Coming Soon")

def export_defaulters_csv(request):
    return HttpResponse("CSV Export Coming Soon")

def send_fee_reminder(request, fee_id):
    return HttpResponse(f"Reminder sent for fee {fee_id}")

def send_bulk_fee_reminders(request):
    return HttpResponse("Bulk reminders sent")


def fees_dashboard(request):
    total_students = StudentProfile.objects.count()

    total_paid = FeePayment.objects.filter(
        status="paid"
    ).aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_pending = FeePayment.objects.filter(
        status="pending"
    ).aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_fees = total_paid + total_pending

    context = {
        "total_students": total_students,
        "total_fees": total_fees,
        "total_paid": total_paid,
        "total_pending": total_pending,
    }

    return render(request, "parents/fees.html", context)