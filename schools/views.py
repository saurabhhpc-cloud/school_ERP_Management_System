from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractMonth, TruncMonth
from django.contrib.auth import get_user_model
from django.utils import timezone
import calendar
from students.models import Student
from fees.models import FeePayment
from attendance.models import Attendance
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from django.db.models import Count, Q
from datetime import date, timedelta


@login_required
def today_attendance(request):
    school = request.user.school
    today = timezone.now().date()

    total_students = Student.objects.filter(school=school).count()
    present = Attendance.objects.filter(
        student__school=school,
        date=today,
        is_present=True
    ).count()

    absent = total_students - present
    percent = round((present / total_students) * 100, 2) if total_students else 0

    return render(
        request,
        "school/today_attendance.html",
        {
            "today_total": total_students,
            "today_present": present,
            "today_absent": absent,
            "today_percentage": percent,
        }
    )
@login_required
def export_attendance_excel(request):
    school = request.user.school
    today = timezone.now().date()

    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"

    ws.append(["Student Name", "Class", "Date", "Status"])

    records = Attendance.objects.filter(student__school=school, date=today)

    for r in records:
        ws.append([
            r.student.name,
            r.student.class_name,
            r.date.strftime("%d-%m-%Y"),
            "Present" if r.is_present else "Absent"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=attendance_today.xlsx"

    wb.save(response)
    return response


# =================
# FEES EXCEL EXPORT
# =================
@login_required
def export_fees_excel(request):
    school = request.user.school

    wb = Workbook()
    ws = wb.active
    ws.title = "Fees"

    ws.append(["Student", "Amount Paid", "Status", "Date"])

    fees = FeePayment.objects.filter(school=school)

    for f in fees:
        ws.append([
            str(f.student) if f.student else "N/A",
            f.amount_paid,
            f.status,
            f.created_at.strftime("%d-%m-%Y")
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=fees_report.xlsx"

    wb.save(response)
    return response


# =====================
# ATTENDANCE PDF EXPORT
# =====================
@login_required
def export_attendance_pdf(request):
    school = request.user.school
    today = timezone.now().date()

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=attendance_today.pdf"

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    y = 800
    p.drawString(50, y, f"Attendance Report - {today.strftime('%d-%m-%Y')}")
    y -= 30

    records = Attendance.objects.filter(student__school=school, date=today)

    for r in records:
        line = f"{r.student.name} | {r.student.class_name} | {'Present' if r.is_present else 'Absent'}"
        p.drawString(50, y, line)
        y -= 20

        if y < 50:
            p.showPage()
            y = 800

    p.save()
    return response


# ===============
# FEES PDF EXPORT
# ===============
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
@login_required
def school_dashboard(request):
    school = request.user.school
    User = get_user_model()
    user = request.user

    today = date.today()
    this_month = today.replace(day=1)
    last_month = (this_month - timedelta(days=1)).replace(day=1)

    # ======================
    # ROLE PERMISSIONS
    # ======================
    can_import_attendance = (
        user.is_superuser or
        user.groups.filter(name__in=["Teacher", "SchoolAdmin"]).exists()
    )

    can_import_students = (
        user.is_superuser or
        user.groups.filter(name="SchoolAdmin").exists()
    )

    # =====================
    # AI ATTENDANCE INSIGHT
    # =====================
    ai_insight = None

    classes = (
        Attendance.objects
        .filter(student__school=school)
        .values_list("student__class_name", flat=True)
        .distinct()
    )

    for class_name in classes:
        this_month_present = Attendance.objects.filter(
            student__school=school,
            student__class_name=class_name,
            date__gte=this_month,
            is_present=True
        ).count()

        last_month_present = Attendance.objects.filter(
            student__school=school,
            student__class_name=class_name,
            date__gte=last_month,
            date__lt=this_month,
            is_present=True
        ).count()

        if last_month_present > 0:
            change = round(
                ((this_month_present - last_month_present) / last_month_present) * 100,
                2
            )

            if change < -5:
                ai_insight = {
                    "type": "danger",
                    "message": f"⚠ Attendance dropped by {abs(change)}% in Class {class_name}"
                }
                break
            elif change > 5:
                ai_insight = {
                    "type": "success",
                    "message": f"✅ Attendance improved by {change}% in Class {class_name}"
                }
                break

    # =================
    # BASIC STATISTICS
    # =================
    total_students = Student.objects.filter(school=school).count()

    today_present = Attendance.objects.filter(
        student__school=school,
        date=today,
        is_present=True
    ).count()

    today_absent = total_students - today_present

    today_percentage = (
        round((today_present / total_students) * 100, 2)
        if total_students else 0
    )

    total_teachers = User.objects.filter(
        is_teacher=True,
        school=school
    ).count()

    # =========
    # FEES DATA
    # =========
    fees_collected = FeePayment.objects.filter(
        school=school,
        status="paid"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    pending_fees = FeePayment.objects.filter(
        school=school,
        status="pending"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    # ====================
    # MONTHLY ATTENDANCE
    # ====================
    attendance_qs = (
        Attendance.objects
        .filter(student__school=school)
        .annotate(month=ExtractMonth("date"))
        .values("month")
        .annotate(
            total=Count("id"),
            present=Count("id", filter=Q(is_present=True))
        )
        .order_by("month")
    )

    attendance_labels = []
    attendance_data = []

    for row in attendance_qs:
        percent = round((row["present"] / row["total"]) * 100, 2)
        attendance_labels.append(calendar.month_abbr[row["month"]])
        attendance_data.append(percent)

    # =========
    # CONTEXT
    # =========
    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,

        "fees_collected": float(fees_collected),
        "pending_fees_amount": float(pending_fees),

        "attendance_labels": attendance_labels,
        "attendance_data": attendance_data,

        "today_total": total_students,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_percentage": today_percentage,

        "ai_insight": ai_insight,

        # 🔐 permissions for sidebar
        "can_import_attendance": can_import_attendance,
        "can_import_students": can_import_students,
    }

    return render(request, "school/school_dashboard.html", context)
