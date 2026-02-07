from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.db.models.functions import ExtractMonth, TruncMonth
from django.contrib.auth import get_user_model
from django.utils import timezone
import calendar
from django.db.models import Avg, F, FloatField, ExpressionWrapper
from exams.models import Result
from admission.models import StudentProfile
from fees.models import FeePayment
from attendance.models import Attendance
from django.http import HttpResponse
from openpyxl import Workbook
from reportlab.pdfgen import canvas
from django.db.models import Count, Q
from datetime import date, timedelta
from admission.models import Admission
from admission.models import StudentProfile
from teacher.models import Teacher

from notices.views import get_notices_for_user

@login_required
def today_attendance(request):
    school = request.user.school
    today = timezone.now().date()

    total_students = StudentProfile.objects.filter(school=school).count()
    present = Attendance.objects.filter(
        student__school=school,
        date=today,
        status="P"
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
    user = request.user
    today = date.today()

    # ======================
    # NOTICES
    # ======================
    notices = get_notices_for_user(user).order_by("-created_at")[:3]

    # ======================
    # CLASS-WISE RESULT ANALYTICS
    # ======================
    result_qs = (
        Result.objects
        .filter(school=school)
        .annotate(
            percentage=ExpressionWrapper(
                (F("marks_obtained") / F("max_marks")) * 100,
                output_field=FloatField()
            )
        )
        .values("exam__class_name")
        .annotate(avg_percentage=Avg("percentage"))
        .order_by("exam__class_name")
    )

    result_labels = []
    result_data = []

    for row in result_qs:
        result_labels.append(row["exam__class_name"])
        result_data.append(round(row["avg_percentage"], 2))

    # ======================
    # STUDENTS & TEACHERS
    # ======================
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = Teacher.objects.filter(user__school=school).count()

    # ======================
    # TODAY ATTENDANCE
    # ======================
    today_present = Attendance.objects.filter(
        student__school=school,
        date=today,
        status="P"
    ).count()

    today_absent = total_students - today_present
    today_percentage = (
        round((today_present / total_students) * 100, 2)
        if total_students else 0
    )

    # ======================
    # FEES
    # ======================
    fees_collected = FeePayment.objects.filter(
        school=school,
        status="paid"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    pending_fees_amount = FeePayment.objects.filter(
        school=school,
        status="pending"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    pending_students_count = (
        FeePayment.objects.filter(
            school=school,
            status="pending"
        )
        .values("student")
        .distinct()
        .count()
    )

    # ======================
    # ADMISSIONS
    # ======================
    admissions = Admission.objects.filter(student__school=school)

    context = {
        "notices": notices,

        "total_students": total_students,
        "total_teachers": total_teachers,

        "today_total": total_students,
        "today_present": today_present,
        "today_absent": today_absent,
        "today_percentage": today_percentage,

        "fees_collected": float(fees_collected),
        "pending_fees_amount": float(pending_fees_amount),
        "pending_students_count": pending_students_count,

        "total_admissions": admissions.count(),
        "enquiry_count": admissions.filter(admission_status="ENQUIRY").count(),
        "applied_count": admissions.filter(admission_status="APPLIED").count(),
        "confirmed_count": admissions.filter(admission_status="CONFIRMED").count(),
        "rejected_count": admissions.filter(admission_status="REJECTED").count(),
        "pending_admissions": admissions.filter(admission_status="APPLIED")[:5],

        # 🔥 CHART DATA
        "result_labels": result_labels,
        "result_data": result_data,
    }

    return render(request, "school/school_dashboard.html", context)

