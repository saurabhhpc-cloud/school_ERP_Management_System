from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.db.models import Count, Q
from django.contrib import messages
from datetime import date
from django.utils.timezone import now
from datetime import datetime
import openpyxl
from django.db.models.functions import TruncMonth
from .models import Attendance
from admission.models import StudentProfile
from teacher.models import Teacher


# ===============================
# ROLE CHECKS (SAFE)
# ===============================

def can_view_attendance(user):
    if not user.is_authenticated:
        return False
    return (
        user.is_superuser or
        user.groups.filter(name__in=["Teacher", "SchoolAdmin"]).exists()
    )


def is_teacher(user):
    if not user.is_authenticated:
        return False
    return user.is_superuser or user.groups.filter(name="Teacher").exists()


# ===============================
# IMPORT ATTENDANCE (EXCEL)
# ===============================

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name__in=["Teacher", "SchoolAdmin"]).exists())
def import_attendance_excel(request):
    school = getattr(request.user, "school", None)
    if not school:
        messages.error(request, "School not assigned.")
        return redirect("/")

    teacher = Teacher.objects.filter(user=request.user).first()
    if not teacher:
        messages.warning(
            request,
            "Teacher profile not found. Attendance will be saved without teacher."
        )

    if request.method == "POST":
        excel_file = request.FILES.get("file")
        if not excel_file:
            messages.error(request, "Please upload Excel file.")
            return redirect("attendance:import")

        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))

        if len(rows) < 2:
            messages.error(request, "Excel has no data rows.")
            return redirect("attendance:import")

        created = 0

        for row in rows[1:]:
            try:
                name, class_name, section, date, status = row
            except ValueError:
                continue

            student = StudentProfile.objects.filter(
                school=school,
                name__iexact=str(name).strip(),
                class_name=str(class_name).strip(),
                section=str(section).strip()
            ).first()

            if not student:
                continue

            is_present = str(status).strip().upper().startswith("P")

            Attendance.objects.create(
                school=school,
                student=student,
                teacher=teacher,
                date=date if isinstance(date, datetime) else timezone.now().date(),
                is_present=is_present
            )
            created += 1

        messages.success(request, f"{created} attendance records imported")
        return redirect("attendance:class_wise")

    return render(request, "attendance/import_attendance.html")



# ===============================
# CLASS WISE ATTENDANCE (TABLE)
# ===============================

@login_required
@user_passes_test(can_view_attendance, login_url="/login/")
def class_wise_attendance(request):
    school = request.user.school

    selected_class = request.GET.get("class_name")
    selected_section = request.GET.get("section")
    selected_date = request.GET.get("date")

    records = Attendance.objects.select_related("student").filter(
        school=school
    )

    if selected_class:
        records = records.filter(student__class_name=selected_class)

    if selected_section:
        records = records.filter(student__section__iexact=selected_section)

    if selected_date:
        records = records.filter(date=selected_date)

    return render(
        request,
        "attendance/class_wise.html",
        {
            "records": records.order_by("-date"),
            "total": records.count(),
            "present": records.filter(status="P").count(),
            "absent": records.filter(status="A").count(),
            "selected_class": selected_class,
            "selected_section": selected_section,
            "selected_date": selected_date,
        },
    )


# ===============================
# ATTENDANCE % (STUDENT WISE)
# ===============================

@login_required
@user_passes_test(is_teacher, login_url="/login/")
def attendance_percentage(request):
    school = request.user.school
    selected_class = request.GET.get("class_name")
    selected_section = request.GET.get("section")

    students = StudentProfile.objects.filter(school=school)

    if selected_class:
        students = students.filter(class_name=selected_class)
    if selected_section:
        students = students.filter(section=selected_section)

    attendance_stats = (
        Attendance.objects
        .filter(student__in=students)
        .values("student")
        .annotate(
            total=Count("id"),
            present=Count("id", filter=Q(status="P"))
        )
    )

    stats_map = {s["student"]: s for s in attendance_stats}

    data = []
    for student in students:
        s = stats_map.get(student.id, {"total": 0, "present": 0})
        total = s["total"]
        present = s["present"]
        percent = round((present / total) * 100, 2) if total else 0

        data.append({
            "student": student,
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


# ===============================
# TODAY ATTENDANCE SUMMARY
# ===============================

@login_required
@user_passes_test(is_teacher, login_url="/login/")
def today_summary(request):
    school = request.user.school
    today = timezone.now().date()

    qs = Attendance.objects.filter(
        school=school,
        date=today
    )

    total_students = qs.values("student").distinct().count()
    present = qs.filter(status="P").count()
    absent = qs.filter(status="A").count()

    attendance_percent = round(
        (present / total_students) * 100, 2
    ) if total_students else 0

    return render(
        request,
        "attendance/summary.html",
        {
            "total_students": total_students,
            "present": present,
            "absent": absent,
            "attendance_percent": attendance_percent,
            "today": today,
        }
    )


# ===============================
# ATTENDANCE OVERVIEW (CLASS+SECTION)
# ===============================

@login_required
def attendance_overview(request):
    school = request.user.school

    # ---- Month filter ----
    month_str = request.GET.get("month")
    if month_str:
        year, month = map(int, month_str.split("-"))
        start_date = date(year, month, 1)
    else:
        today = now().date()
        start_date = date(today.year, today.month, 1)

    # Next month calculation
    if start_date.month == 12:
        end_date = date(start_date.year + 1, 1, 1)
    else:
        end_date = date(start_date.year, start_date.month + 1, 1)

    class_sections = (
        StudentProfile.objects
        .filter(school=school)
        .values("class_name", "section")
        .distinct()
        .order_by("class_name", "section")
    )

    overview = []
    chart_labels = []
    chart_data = []

    for cs in class_sections:
        class_name = cs["class_name"]
        section = cs["section"]

        # 🔥 DATE FILTER APPLIED HERE
        qs = Attendance.objects.filter(
            school=school,
            student__class_name=class_name,
            student__section=section,
            date__gte=start_date,
            date__lt=end_date
        )

        total = qs.count()
        present = qs.filter(status="P").count()
        percent = round((present / total) * 100, 2) if total else 0

        overview.append({
            "class_name": class_name,
            "section": section,
            "total": total,
            "present": present,
            "percent": percent,
        })

        if total > 0:
            chart_labels.append(f"{class_name}-{section}")
            chart_data.append(float(percent))

    return render(
        request,
        "attendance/overview.html",
        {
            "overview": overview,
            "chart_labels": chart_labels,
            "chart_data": chart_data,
            "selected_month": start_date.strftime("%Y-%m"),
        }
    )

from datetime import date
from django.utils.timezone import now

@login_required
def low_attendance_alerts(request):
    school = request.user.school

    # Month filter
    month_str = request.GET.get("month")
    if month_str:
        year, month = map(int, month_str.split("-"))
        start_date = date(year, month, 1)
    else:
        today = now().date()
        start_date = date(today.year, today.month, 1)

    end_date = (
        date(start_date.year + 1, 1, 1)
        if start_date.month == 12
        else date(start_date.year, start_date.month + 1, 1)
    )

    alerts = []

    students = StudentProfile.objects.filter(school=school)

    for student in students:
        qs = Attendance.objects.filter(
            student=student,
            date__gte=start_date,
            date__lt=end_date
        )

        total = qs.count()
        present = qs.filter(status="P").count()

        if total == 0:
            continue

        percent = round((present / total) * 100, 2)

        if percent < 75:
            alerts.append({
                "student": student,
                "class_name": student.class_name,
                "section": student.section,
                "total": total,
                "present": present,
                "percent": percent,
            })

    return render(
        request,
        "attendance/low_attendance.html",
        {
            "alerts": alerts,
            "selected_month": start_date.strftime("%Y-%m"),
        }
    )

@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name="SchoolAdmin").exists())
def student_monthly_attendance(request):
    school = request.user.school
    student_id = request.GET.get("student")

    students = StudentProfile.objects.filter(school=school)

    labels = []
    data = []
    selected_student = None

    if student_id:
        selected_student = students.filter(id=student_id).first()

        if selected_student:
            year = now().year

            for month in range(1, 13):
                start = date(year, month, 1)
                end = (
                    date(year + 1, 1, 1)
                    if month == 12
                    else date(year, month + 1, 1)
                )

                qs = Attendance.objects.filter(
                    student=selected_student,
                    date__gte=start,
                    date__lt=end
                )

                total = qs.count()
                present = qs.filter(status="P").count()
                percent = round((present / total) * 100, 2) if total else 0

                labels.append(start.strftime("%b"))
                data.append(percent)

    return render(
        request,
        "attendance/student_monthly.html",
        {
            "students": students,
            "labels": labels,
            "data": data,
            "selected_student": selected_student,
        }
    )

@login_required
def mark_attendance(request):
    teacher = Teacher.objects.get(user=request.user)
    today = timezone.now().date()

    students = StudentProfile.objects.filter(
        class_name=teacher.class_name,
        section=teacher.section,
        school=request.user.school
    )

    if request.method == "POST":
        for student in students:
            status = request.POST.get(str(student.id))
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={
                    "is_present": True if status == "P" else False,
                    "school": request.user.school,
                    "teacher": teacher
                }
            )
        return redirect("teachers:dashboard")

    return render(
        request,
        "attendance/mark_attendance.html",
        {"students": students}
    )
