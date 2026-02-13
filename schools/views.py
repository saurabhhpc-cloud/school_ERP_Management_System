from django.shortcuts import render, redirect
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
from datetime import date, timedelta
from teacher.models import Teacher
from django.db.models import Avg, Count, Q, F, FloatField, ExpressionWrapper
from admission.models import StudentProfile, Admission
from notices.views import get_notices_for_user
import json
from django.db.models.functions import TruncMonth
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse

# TODAY ATTENDANCE
# =====================================================
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

    percent = round((present / total_students) * 100, 1) if total_students else 0

    return render(request, "school/today_attendance.html", {
        "today_total": total_students,
        "today_present": present,
        "today_absent": total_students - present,
        "today_percentage": percent,
    })

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
    user = request.user
    school = user.school
    today = date.today()

    # ================= BASIC COUNTS =================
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = Teacher.objects.filter(user__school=school).count()

    # ================= ATTENDANCE =================
    today_present = Attendance.objects.filter(
        student__school=school,
        date=today,
        status="P"
    ).count()

    today_absent = total_students - today_present if total_students else 0

    today_percentage = round(
        (today_present / total_students) * 100, 1
    ) if total_students else 0

    # ================= FEES =================
    fees_collected = (
        FeePayment.objects
        .filter(school=school, status="paid")
        .aggregate(total=Sum("amount_paid"))["total"] or 0
    )

    pending_fees_amount = (
        FeePayment.objects
        .filter(school=school, status="pending")
        .aggregate(total=Sum("amount_paid"))["total"] or 0
    )

    # ================= RESULT CHART =================
    results = (
        Result.objects
        .filter(student__school=school)
        .values("student__admission__class_applied")
        .annotate(
            avg_percentage=Avg(
                ExpressionWrapper(
                    (F("marks_obtained") / F("marks_obtained")) * 100,
                    output_field=FloatField()
                )
            )
        )
    )

    result_labels = []
    result_data = []

    for r in results:
        result_labels.append(r["student__admission__class_applied"])
        result_data.append(round(r["avg_percentage"], 1))
    
    # ================= MONTHLY FEES TREND =================
    six_months_ago = today - timedelta(days=180)

    monthly = (
        FeePayment.objects
        .filter(school=school, status="paid", created_at__gte=six_months_ago)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Sum("amount_paid"))
        .order_by("month")
    )

    monthly_labels = []
    monthly_data = []

    for m in monthly:
        monthly_labels.append(m["month"].strftime("%b"))
        monthly_data.append(float(m["total"]))

    # ================= HEATMAP =================
    heatmap = []

    attendance_records = (
        Attendance.objects
        .filter(student__school=school)
        .values("date")
        .annotate(
            total=Count("id"),
            present=Count("id", filter=Q(status="P"))
        )
        .order_by("-date")[:12]
    )

    for record in attendance_records:
        percentage = (record["present"] / record["total"]) * 100 if record["total"] else 0
        heatmap.append({
            "date": record["date"].strftime("%d %b"),
            "percentage": round(percentage, 1),
            "opacity": round(percentage / 100, 2)
        })

    # ================= FORECAST =================
    forecast_revenue = 0
    if len(monthly_data) >= 3:
        forecast_revenue = sum(monthly_data[-3:]) / 3

    drop_alert = False
    if len(monthly_data) >= 2:
        drop_alert = monthly_data[-1] < monthly_data[-2]
    # ================= SCHOOL HEALTH SCORE =================

    health_score = 0

    if total_students:
        attendance_score = today_percentage
    else:
        attendance_score = 0

    if fees_collected + pending_fees_amount:
        fee_ratio = (fees_collected / (fees_collected + pending_fees_amount)) * 100
    else:
        fee_ratio = 100

    health_score = round((attendance_score * 0.6) + (fee_ratio * 0.4), 1)


    context = {
        "total_students": total_students,
        "total_teachers": total_teachers,
        "today_percentage": today_percentage,
        "today_present": today_present,
        "today_absent": today_absent,
        "fees_collected": fees_collected,
        "pending_fees_amount": pending_fees_amount,
        "result_labels": json.dumps(result_labels),
        "result_data": json.dumps(result_data),
        "monthly_labels": json.dumps(monthly_labels),
        "monthly_data": json.dumps(monthly_data),
        "heatmap_data": heatmap,
        "forecast_revenue": round(forecast_revenue, 2),
        "drop_alert": drop_alert,
        "health_score": health_score,
    }

    return render(request, "school/school_dashboard.html", context)



@login_required
def principal_dashboard(request):
    user = request.user

    if not user.groups.filter(name__iexact="principal").exists():
        return redirect("schools:dashboard")

    school = user.school

    class_data = []
    total_students = 0
    total_present = 0
    total_attendance_records = 0
    total_result_sum = 0
    result_count = 0

    classes = (
        Admission.objects
        .filter(student__school=school)
        .values_list("class_applied", flat=True)
        .distinct()
    )

    for cls in classes:
        students = StudentProfile.objects.filter(
            school=school,
            admission__class_applied=cls
        )

        student_count = students.count()
        total_students += student_count

        total_att = Attendance.objects.filter(student__in=students).count()
        present_att = Attendance.objects.filter(student__in=students, status="P").count()

        total_attendance_records += total_att
        total_present += present_att

        avg_attendance = (
            (present_att / total_att) * 100
        ) if total_att else None

        avg_result = (
            Result.objects
            .filter(student__in=students)
            .annotate(
                percentage=ExpressionWrapper(
                    (F("marks_obtained") / F("marks_obtained")) * 100,
                    output_field=FloatField()
                )
            )
            .aggregate(avg=Avg("percentage"))["avg"]
        )

        if avg_result is not None:
            total_result_sum += avg_result
            result_count += 1

        class_data.append({
            "class": cls,
            "students": student_count,
            "sections": students.values("admission__section").distinct().count(),
            "avg_attendance": round(avg_attendance, 1) if avg_attendance else "N/A",
            "avg_result": round(avg_result, 1) if avg_result else "N/A",
        })

    overall_attendance = (
        (total_present / total_attendance_records) * 100
    ) if total_attendance_records else 0

    overall_result = (
        total_result_sum / result_count
    ) if result_count else 0

    return render(request, "school/principal_dashboard.html", {
        "class_data": class_data,
        "total_students": total_students,
        "overall_attendance": round(overall_attendance, 1),
        "overall_result": round(overall_result, 1),
        "is_principal": True,
    })


# =====================================================
# SECTION-WISE DRILLDOWN
# =====================================================
@login_required
def principal_class_sections(request, class_name):
    user = request.user

    if not user.groups.filter(name="principal").exists():
        return redirect("schools:dashboard")

    school = user.school
    section_data = []

    sections = (
        StudentProfile.objects
        .filter(
            school=school,
            admission__class_applied=class_name
        )
        .values_list("admission__section", flat=True)
        .distinct()
    )

    for sec in sections:
        students = StudentProfile.objects.filter(
            school=school,
            admission__class_applied=class_name,
            admission__section=sec
        )

        total_att = Attendance.objects.filter(student__in=students).count()
        present_att = Attendance.objects.filter(student__in=students, status="P").count()

        avg_attendance = (
            (present_att / total_att) * 100
        ) if total_att else None

        avg_result = (
            Result.objects
            .filter(student__in=students)
            .annotate(
                percentage=ExpressionWrapper(
                    (F("marks_obtained") / F("marks_obtained")) * 100,
                    output_field=FloatField()
                )
            )
            .aggregate(avg=Avg("percentage"))["avg"]
        )

        if avg_attendance is None:
            status = "Pending"
        elif avg_attendance >= 85:
            status = "Strong"
        elif avg_attendance >= 75:
            status = "Watch"
        else:
            status = "Critical"

        section_data.append({
            "section": sec,
            "students": students.count(),
            "avg_attendance": round(avg_attendance, 1) if avg_attendance else "N/A",
            "avg_result": round(avg_result, 1) if avg_result else "N/A",
            "status": status,
        })

    return render(request, "school/principal_class_sections.html", {
        "class_name": class_name,
        "section_data": section_data,
        "is_principal": True,
    })



@login_required
def download_analytics_pdf(request):
    school = request.user.school

    # Basic data
    total_students = StudentProfile.objects.filter(school=school).count()
    total_teachers = Teacher.objects.filter(user__school=school).count()

    fees_collected = (
        FeePayment.objects
        .filter(school=school, status="paid")
        .aggregate(total=Sum("amount_paid"))["total"] or 0
    )

    # Create response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=school_analytics_report.pdf"

    doc = SimpleDocTemplate(response)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("School Analytics Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Total Students: {total_students}", styles["Normal"]))
    elements.append(Paragraph(f"Total Teachers: {total_teachers}", styles["Normal"]))
    elements.append(Paragraph(f"Fees Collected: ₹ {fees_collected}", styles["Normal"]))

    doc.build(elements)

    return response
