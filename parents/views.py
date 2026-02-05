from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import render
from students.models import Student
from attendance.models import Attendance
from fees.models import FeePayment
from django.db.models import Sum


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
        # FEES
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

        # ATTENDANCE (safe)
        attendance_records = Attendance.objects.filter(student=child)
        if attendance_records.exists():
            present = attendance_records.filter(status="Present").count()
            total = attendance_records.count()
            attendance = int((present / total) * 100)
            attendance_sum += attendance
            attendance_count += 1
        else:
            attendance = None

        child_cards.append({
            "name": child.full_name,
            "class": child.class_name,
            "attendance": attendance,
            "paid": paid,
            "pending": pending,
        })

    avg_attendance = (
        int(attendance_sum / attendance_count)
        if attendance_count > 0 else None
    )

    context = {
        "total_children": total_children,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "avg_attendance": avg_attendance,
        "child_cards": child_cards,
    }

    return render(request, "parents/parent.html", context)

@login_required
def parent_fees(request, student_id):
    student = get_object_or_404(Student, id=student_id)
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


