import csv
from django.db.models import Sum
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.http import HttpResponse
from django.shortcuts import render

from .models import StudentFee
from django.shortcuts import redirect
from .services.whatsapp import send_whatsapp
from .utils import fee_reminder_message
from django.contrib import messages

def is_accountant(user):
    return (
        user.is_superuser or
        user.groups.filter(name="Accountant").exists() or
        user.groups.filter(name="Demo").exists()
    )

@login_required
@user_passes_test(is_accountant, login_url="/login/")
def defaulters_report(request):
    selected_class = request.GET.get("class_name")
    selected_status = request.GET.get("status", "Due")

    qs = StudentFee.objects.select_related("student").exclude(status="Paid")

    if selected_class:
        qs = qs.filter(student__class_name=selected_class)

    if selected_status:
        qs = qs.filter(status=selected_status)

    # ✅ DEMO CHECK (INSIDE FUNCTION)
    is_demo = request.user.groups.filter(name="Demo").exists()

    return render(
        request,
        "fees/defaulters.html",
        {
            "records": qs,
            "selected_class": selected_class,
            "selected_status": selected_status,
            "is_demo": is_demo,   # 👈 NOW CORRECT
        }
    )
@login_required
@user_passes_test(is_accountant, login_url="/login/")
def export_defaulters_csv(request):

    if request.user.groups.filter(name="Demo").exists():
        return HttpResponseForbidden("Demo users cannot export data")
    selected_class = request.GET.get("class_name")
    selected_status = request.GET.get("status", "Due")

    qs = StudentFee.objects.select_related("student").exclude(status="Paid")

    if selected_class:
        qs = qs.filter(student__class_name=selected_class)

    if selected_status:
        qs = qs.filter(status=selected_status)

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="fee_defaulters.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Student Name",
        "Class",
        "Total Amount",
        "Paid Amount",
        "Due Amount",
        "Status",
        "Due Date"
    ])

    for r in qs:
        writer.writerow([
            r.student.full_name,
            r.student.class_name,
            r.total_amount,
            r.paid_amount,
            r.due_amount,
            r.status,
            r.due_date
        ])

    return response
@login_required
@user_passes_test(is_accountant, login_url="/login/")
def send_fee_reminder(request, fee_id):

    if request.user.groups.filter(name="Demo").exists():
        return HttpResponseForbidden("Demo users cannot send reminders")
    fee = StudentFee.objects.select_related("student").get(id=fee_id)

    phone = fee.student.parent_mobile

    msg = fee_reminder_message(
        student_name=fee.student.full_name,
        total=fee.total_amount,
        paid=fee.paid_amount,
        due=fee.due_amount,
        due_date=fee.due_date,
    )

    send_whatsapp(phone, msg)

    messages.success(
        request,
        f"WhatsApp reminder sent to {fee.student.full_name}"
    )

    return redirect("defaulters_report")

@login_required
@user_passes_test(is_accountant, login_url="/login/")
def send_bulk_fee_reminders(request):

    if request.user.groups.filter(name="Demo").exists():
        return HttpResponseForbidden("Demo users cannot send reminders")
    selected_class = request.GET.get("class_name")
    selected_status = request.GET.get("status", "Due")

    qs = StudentFee.objects.select_related("student").exclude(status="Paid")

    if selected_class:
        qs = qs.filter(student__class_name=selected_class)

    if selected_status:
        qs = qs.filter(status=selected_status)

    count = 0

    for fee in qs:
        phone = fee.student.parent_mobile
        if not phone:
            continue

        msg = fee_reminder_message(
            student_name=fee.student.full_name,
            total=fee.total_amount,
            paid=fee.paid_amount,
            due=fee.due_amount,
            due_date=fee.due_date,
        )

        send_whatsapp(phone, msg)
        count += 1

    messages.success(
        request,
        f"Bulk WhatsApp sent to {count} parents"
    )

    return redirect("defaulters_report")

@login_required
@user_passes_test(is_accountant, login_url="/login/")
def fees_dashboard(request):
    qs = StudentFee.objects.select_related("student")

    total_students = qs.values("student").distinct().count()
    total_amount = qs.aggregate(Sum("total_amount"))["total_amount__sum"] or 0
    paid_amount = qs.aggregate(Sum("paid_amount"))["paid_amount__sum"] or 0
    due_amount = total_amount - paid_amount

    defaulters_count = qs.exclude(status="Paid").count()

    return render(
        request,
        "fees/dashboard.html",
        {
            "total_students": total_students,
            "total_amount": total_amount,
            "paid_amount": paid_amount,
            "due_amount": due_amount,
            "defaulters_count": defaulters_count,
        }
    )
