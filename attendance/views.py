from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.db.models import Count

from .models import Attendance
from students.models import Student


# 🔐 ROLE CHECK
def is_teacher(user):
    """
    Allow access only to Teacher group OR Superuser (Admin)
    """
    return user.is_superuser or user.groups.filter(name="Teacher").exists()


# -------------------------------
# CLASS WISE ATTENDANCE
# -------------------------------
@login_required
@user_passes_test(is_teacher, login_url="/login/")
# -------------------------------
# CLASS WISE ATTENDANCE (DASHBOARD)
# -------------------------------
@login_required
@user_passes_test(is_teacher, login_url="/login/")

def class_wise_attendance(request):
    selected_class = request.GET.get("class_name")
    selected_section = request.GET.get("section")
    selected_date = request.GET.get("date")

    records = Attendance.objects.select_related("student")

    if selected_class:
        records = records.filter(student__class_name=selected_class)

    if selected_section:
         records = records.filter(student__section__iexact=selected_section)

    if selected_date:
        records = records.filter(date=selected_date)

    # 🔢 SUMMARY COUNTS (FOR DASHBOARD CARDS)
    total = records.count()
    present = records.filter(status="Present").count()
    absent = records.filter(status="Absent").count()

    return render(
        request,
        "attendance/class_wise.html",
        {
            "records": records,
            "total": total,
            "present": present,
            "absent": absent,
            "selected_class": selected_class,
            "selected_section": selected_section,
            "selected_date": selected_date,
        },
    )



# -------------------------------
# ATTENDANCE PERCENTAGE
# -------------------------------
@login_required
@user_passes_test(is_teacher, login_url="/login/")
def attendance_percentage(request):
    selected_class = request.GET.get("class_name")
    selected_section = request.GET.get("section")

    students = Student.objects.all()

    if selected_class:
        students = students.filter(class_name=selected_class)
    if selected_section:
        students = students.filter(section=selected_section)

    data = []
    for s in students:
        total = Attendance.objects.filter(student=s).count()
        present = Attendance.objects.filter(student=s, status="Present").count()
        percent = round((present / total) * 100, 2) if total > 0 else 0

        data.append({
            "student": s,
            "total": total,
            "present": present,
            "percent": percent,
            "low": percent < 75 and total > 0
        })

    return render(
        request,
        "attendance/percentage.html",
        {
            "data": data,
            "selected_class": selected_class,
            "selected_section": selected_section,
        }
    )


# -------------------------------
# TODAY SUMMARY
# -------------------------------
@login_required
@user_passes_test(is_teacher, login_url="/login/")
def today_summary(request):
    from datetime import date
    today = date.today()

    qs = Attendance.objects.filter(date=today)
    total_students = qs.values("student").distinct().count()
    present = qs.filter(status="Present").count()
    absent = qs.filter(status="Absent").count()

    return render(
        request,
        "attendance/summary.html",
        {
            "total_students": total_students,
            "present": present,
            "absent": absent,
            "today": today,
        }
    )
