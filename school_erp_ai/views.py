from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from admission.models import StudentProfile
from fees.models import FeePayment
from attendance.models import Attendance

@login_required
def saas_dashboard(request):

    total_students = StudentProfile.objects.count()

    fees_collected = FeePayment.objects.filter(
        status="PAID"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    pending_fees = FeePayment.objects.filter(
        status="PENDING"
    ).aggregate(total=Sum("amount_paid"))["total"] or 0

    total_attendance = Attendance.objects.count()
    present_attendance = Attendance.objects.filter(status="PRESENT").count()

    attendance_percent = (
        (present_attendance / total_attendance) * 100
        if total_attendance > 0 else 0
    )

    # 🧠 SIMPLE AI LOGIC
    if attendance_percent < 60:
        ai_insight = "⚠️ Attendance is low. Risk of dropouts detected."
    elif pending_fees > 50000:
        ai_insight = "💰 High pending fees. Follow up with parents."
    else:
        ai_insight = "✅ School performance is stable."

    context = {
        "total_students": total_students,
        "fees_collected": fees_collected,
        "pending_fees": pending_fees,
        "attendance_percent": round(attendance_percent, 1),
        "ai_insight": ai_insight,
    }

    return render(request, "school_admin/dashboard.html", context)
@login_required
def dashboard_view(request):
    return render(request, "school_admin/dashboard.html")


@login_required
def attendance_view(request):
    return render(request, "school_admin/attendance.html")


@login_required
def fees_view(request):
    return render(request, "school_admin/fees.html")


@login_required
def students_view(request):
    return render(request, "school_admin/students.html")


@login_required
def exams_view(request):
    return render(request, "school_admin/exams.html")


@login_required
def reports_view(request):
    return render(request, "school_admin/reports.html")


@login_required
def settings_view(request):
    return render(request, "school_admin/dashboard.html")
