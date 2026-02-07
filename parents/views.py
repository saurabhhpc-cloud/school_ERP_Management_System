from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from admission.models import StudentProfile
from attendance.models import Attendance
from fees.models import FeePayment
from django.db.models import Sum
from notices.views import get_notices_for_user


@login_required
def parent_dashboard(request):

    if not request.user.is_parent:
        return redirect("login")

    parent = request.user
    children = parent.children.all()

    total_children = children.count()
    total_paid = 0
    total_pending = 0
    attendance_sum = 0
    attendance_count = 0

    child_cards = []

    for child in children:

        # 💰 FEES
        paid = 0
        pending = 0
        payments = FeePayment.objects.filter(student=child)

        for p in payments:
            if p.status == "paid":
                paid += p.amount_paid
            else:
                pending += p.amount_paid

        total_paid += paid
        total_pending += pending

        # 📝 ATTENDANCE
        records = Attendance.objects.filter(student=child)
        if records.exists():
            present = records.filter(status="Present").count()
            total = records.count()
            attendance = int((present / total) * 100)
            attendance_sum += attendance
            attendance_count += 1
        else:
            attendance = None

        child_cards.append({
            "name": child.full_name,
            "class": f"{child.class_name}{child.section}",
            "attendance": attendance,
            "paid": paid,
            "pending": pending,
        })

    avg_attendance = (
        int(attendance_sum / attendance_count)
        if attendance_count > 0 else None
    )

    # 🔔 NOTICES (NEW FEATURE)
    notices = get_notices_for_user(request.user).order_by("-created_at")[:5]

    context = {
        "total_children": total_children,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "avg_attendance": avg_attendance,
        "child_cards": child_cards,
        "notices": notices,   # 👈 IMPORTANT
    }

    return render(request, "parents/dashboard.html", context)
@login_required
def parent_fees(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    payments = FeePayment.objects.filter(student=student)

    total_paid = payments.filter(status="paid").aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    total_pending = payments.filter(status="pending").aggregate(
        total=Sum("amount_paid")
    )["total"] or 0

    context = {
        "student": student,
        "payments": payments,
        "total_paid": total_paid,
        "total_pending": total_pending,
    }

    return render(request, "parents/fees.html", context)

def parent_logout(request):
    logout(request)
    return redirect("login")


