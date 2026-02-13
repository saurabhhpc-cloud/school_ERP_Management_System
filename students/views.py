import openpyxl
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from admission.models import StudentProfile, Admission
from attendance.models import Attendance
from exams.models import Result
from fees.models import FeePayment
from admission.models import ParentProfile
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Max
from django.shortcuts import get_object_or_404

@login_required
def edit_student(request, student_id):

    school = request.user.school

    student = get_object_or_404(
        StudentProfile,
        id=student_id,
        school=school
    )

    # Update Parent
    parent = student.parent
    parent.father_name = request.POST.get("father_name")
    parent.mother_name = request.POST.get("mother_name")
    parent.primary_mobile = request.POST.get("primary_mobile")
    parent.email = request.POST.get("email")
    parent.save()

    # Update Student
    student.first_name = request.POST.get("first_name")
    student.last_name = request.POST.get("last_name")
    student.save()

    # Update Admission
    admission = student.admission
    admission.class_applied = request.POST.get("class_applied")
    admission.section = request.POST.get("section")
    admission.save()

    return JsonResponse({
        "success": True,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "class": admission.class_applied,
        "section": admission.section,
    })


@require_POST
@login_required
def toggle_status(request, student_id):

    school = request.user.school

    student = get_object_or_404(
        StudentProfile,
        id=student_id,
        school=school
    )

    student.is_active = not student.is_active
    student.save()

    return JsonResponse({
        "success": True,
        "is_active": student.is_active
    })




# ===============================
# STUDENT LIST
# ===============================
@login_required
def students_list(request):

    school = request.user.school

    students = StudentProfile.objects.filter(
        school=school
    ).select_related("admission")

    class_filter = request.GET.get("class")
    section_filter = request.GET.get("section")
    search_query = request.GET.get("search")

    if class_filter:
        students = students.filter(admission__class_applied=class_filter)

    if section_filter:
        students = students.filter(admission__section=section_filter)

    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    classes = Admission.objects.filter(
        student__school=school
    ).values_list("class_applied", flat=True).distinct()

    sections = Admission.objects.filter(
        student__school=school
    ).values_list("section", flat=True).distinct()

    return render(request, "students/students_list.html", {
        "students": students,
        "classes": classes,
        "sections": sections,
    })


# ===============================
# STUDENT REPORT
# ===============================
@login_required
def student_report(request, student_id):

    school = request.user.school

    student = get_object_or_404(
        StudentProfile,
        id=student_id,
        school=school
    )

    attendance = Attendance.objects.filter(student=student)
    results = Result.objects.filter(student=student)
    payments = FeePayment.objects.filter(student=student)

    total_present = attendance.filter(status="P").count()
    total_days = attendance.count()

    attendance_percentage = (
        round((total_present / total_days) * 100, 1)
        if total_days > 0 else 0
    )

    total_paid = sum(p.amount_paid for p in payments)

    return render(request, "students/report.html", {
        "student": student,
        "attendance_percentage": attendance_percentage,
        "results": results,
        "total_paid": total_paid,
    })

from django.db.models import Max
from django.db.models import Max
from django.db import transaction

@login_required
@transaction.atomic
def add_student(request):

    school = getattr(request.user, "school", None)

    if not school:
        messages.error(request, "No school assigned to this user.")
        return redirect("students:students_list")

    if request.method == "POST":

        # -------------------------
        # Academic Data
        # -------------------------
        academic_year = request.POST.get("academic_year")
        class_applied = request.POST.get("class_applied")
        section = request.POST.get("section")
        admission_type = request.POST.get("admission_type")

        # -------------------------
        # Parent (Duplicate Safe)
        # -------------------------
        parent, created = ParentProfile.objects.get_or_create(
            primary_mobile=request.POST.get("primary_mobile"),
            defaults={
                "father_name": request.POST.get("father_name"),
                "mother_name": request.POST.get("mother_name"),
                "email": request.POST.get("email"),
            }
        )

        # -------------------------
        # AUTO ROLL NUMBER (Per Class)
        # -------------------------
        last_roll = StudentProfile.objects.filter(
            school=school,
            admission__class_applied=class_applied
        ).aggregate(Max("roll_number"))["roll_number__max"]

        next_roll = (last_roll or 0) + 1

        # -------------------------
        # Create Student
        # -------------------------
        student = StudentProfile.objects.create(
            school=school,
            parent=parent,
            first_name=request.POST.get("first_name"),
            last_name=request.POST.get("last_name"),
            gender=request.POST.get("gender"),
            date_of_birth=request.POST.get("date_of_birth"),
            roll_number=next_roll,
            is_active=True
        )

        # -------------------------
        # AUTO ADMISSION NUMBER
        # Format: SCHOOLCODE-YY-0001
        # -------------------------
        year_short = academic_year.split("-")[0][-2:] if academic_year else "25"
        
        last_adm = Admission.objects.filter(
            student__school=school,
            academic_year=academic_year
        ).aggregate(Max("admission_no"))

        last_number = 0

        if last_adm["admission_no__max"]:
            try:
                last_number = int(last_adm["admission_no__max"].split("-")[-1])
            except:
                last_number = 0

        next_adm_number = last_number + 1

        admission_no = f"{school.id}-{year_short}-{next_adm_number:04d}"
        # -------------------------
        # Create Admission
        # -------------------------
        Admission.objects.create(
            student=student,
            academic_year=academic_year,
            class_applied=class_applied,
            section=section,
            admission_type=admission_type,
            admission_status="CONFIRMED",
            admission_no=admission_no
        )

        messages.success(request, "Student added successfully!")

        return redirect("students:students_list")

    return render(request, "students/add_student.html")

# ===============================
# IMPORT EXISTING STUDENTS
# ===============================
@login_required
def import_students_excel(request):

    school = request.user.school

    if request.method == "POST":
        excel_file = request.FILES.get("file")

        wb = openpyxl.load_workbook(excel_file)
        sheet = wb.active
        rows = list(sheet.iter_rows(values_only=True))

        header = [str(h).strip().lower() for h in rows[0]]

        expected_header = [
            "first_name",
            "last_name",
            "gender",
            "dob",
        ]

        if header != expected_header:
            messages.error(
                request,
                "Excel format should be: first_name | last_name | gender | dob"
            )
            return redirect("students:import_students")

        created = 0

        for row in rows[1:]:
            first_name, last_name, gender, dob = row

            StudentProfile.objects.create(
                school=school,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                date_of_birth=dob,
                parent=None,  # For onboarding, can improve later
            )

            created += 1

        messages.success(
            request,
            f"{created} students imported successfully."
        )

        return redirect("students:students_list")

    return render(request, "students/import_students.html")

@login_required
def ajax_filter_students(request):

    school = request.user.school

    students = StudentProfile.objects.filter(
        school=school
    ).select_related("admission")

    class_filter = request.GET.get("class")
    section_filter = request.GET.get("section")
    search_query = request.GET.get("search")

    if class_filter:
        students = students.filter(admission__class_applied=class_filter)

    if section_filter:
        students = students.filter(admission__section=section_filter)

    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    return render(
        request,
        "students/partials/student_rows.html",
        {"students": students}
    )