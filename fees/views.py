from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.db.models import Sum
from .models import FeePayment
import csv
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from fees.models import FeePayment
from django.utils import timezone


@login_required
def export_fees_excel(request):
    school = request.user.school

    wb = Workbook()
    ws = wb.active
    ws.title = "Fees Report"

    ws.append(["Student", "Amount Paid", "Status", "Date"])

    fees = FeePayment.objects.filter(school=school)

    for f in fees:
        ws.append([
            str(f.student) if f.student else "N/A",
            f.amount_paid,
            f.status,
            f.created_at.strftime("%d-%m-%Y"),
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=fees_report.xlsx"

    wb.save(response)
    return response

# FEES PDF EXPORT
# ======================
@login_required
def export_fees_pdf(request):
    school = request.user.school

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=fees_report.pdf"

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(50, y, "Fees Report")
    y -= 30

    fees = FeePayment.objects.filter(school=school)

    for f in fees:
        line = f"{f.student if f.student else 'N/A'} | ₹{f.amount_paid} | {f.status}"
        p.drawString(50, y, line)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response

def fees_dashboard(request):
    school = request.user.school

    total_collected = FeePayment.objects.filter(
        school=school,
        status="paid"
    ).aggregate(Sum("amount_paid"))["amount_paid__sum"] or 0

    pending_count = FeePayment.objects.filter(
        school=school,
        status="pending"
    ).count()

    context = {
        "total_collected": total_collected,
        "pending_count": pending_count,
    }
    return render(request, "fees/dashboard.html", context)


def defaulters_report(request):
    school = request.user.school
    class_name = request.GET.get("class_name", "")
    status = request.GET.get("status", "Due")

    qs = FeePayment.objects.filter(
        school=school
    ).select_related("student")

    records = []

    for fee in qs:
        total = getattr(fee, "total_fee", fee.amount_paid)
        paid = fee.amount_paid
        due = total - paid

        if due <= 0:
            continue

        record_status = "Partial" if paid > 0 else "Due"

        if status and record_status != status:
            continue

        if class_name and fee.student.class_name != class_name:
            continue

        records.append({
            "id": fee.id,
            "student": fee.student,
            "total_amount": total,
            "paid_amount": paid,
            "due_amount": due,
            "status": record_status,
            "due_date": fee.created_at.date(),
        })

    context = {
        "records": records,
        "selected_class": class_name,
        "selected_status": status,
        "is_demo": False,
    }

    return render(request, "fees/defaulters.html", context)


def export_defaulters_csv(request):
    school = request.user.school
    class_name = request.GET.get("class_name", "")
    status = request.GET.get("status", "Due")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="fee_defaulters.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Student", "Class", "Total", "Paid", "Due", "Status", "Due Date"
    ])

    qs = FeePayment.objects.filter(school=school).select_related("student")

    for fee in qs:
        total = getattr(fee, "total_fee", fee.amount_paid)
        paid = fee.amount_paid
        due = total - paid

        if due <= 0:
            continue

        record_status = "Partial" if paid > 0 else "Due"

        if status and record_status != status:
            continue

        if class_name and fee.student.class_name != class_name:
            continue

        writer.writerow([
            fee.student.full_name,
            fee.student.class_name,
            total,
            paid,
            due,
            record_status,
            fee.created_at.date(),
        ])

    return response



def send_fee_reminder(request, fee_id):
    fee = get_object_or_404(FeePayment, id=fee_id)
    # 🔔 future: WhatsApp / SMS / Email
    return redirect(request.META.get("HTTP_REFERER", "/fees/defaulters/"))


def send_bulk_fee_reminders(request):
    # 🔔 future: WhatsApp API integration
    return redirect("/fees/defaulters/")
