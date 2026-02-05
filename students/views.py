import openpyxl

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import Student

@login_required 
def student_list(request): 
    students = Student.objects.filter( school=request.user.school )
    return render( 
        request, 
        "students/student_list.html", 
        {"students": students} 
        )

@login_required
def import_students_excel(request):

    # 🔐 School guard (best practice)
    school = request.user.school
    if not school:
        messages.error(request, "School not assigned to your account.")
        return redirect("dashboard")

    if request.method == "POST":
        excel_file = request.FILES.get("file")

        if not excel_file:
            messages.error(request, "Please upload a valid Excel file.")
            return redirect("students:import_students")

        try:
            wb = openpyxl.load_workbook(excel_file)
            sheet = wb.active
        except Exception:
            messages.error(request, "Invalid Excel file.")
            return redirect("students:import_students")

        rows = list(sheet.iter_rows(values_only=True))

        if not rows:
            messages.error(request, "Excel file is empty.")
            return redirect("students:import_students")

        # ✅ Safe header handling
        header = tuple(
            str(h).strip().lower() if h else ""
            for h in rows[0]
        )

        expected_header = ("name", "class_name", "section")

        if header != expected_header:
            messages.error(
                request,
                "Invalid Excel format. Headers must be: name | class_name | section"
            )
            return redirect("students:import_students")

        created = 0
        skipped = 0

        for row in rows[1:]:
            name, class_name, section = row

            if not all([name, class_name, section]):
                skipped += 1
                continue

            if Student.objects.filter(
                school=school,
                name__iexact=str(name).strip(),
                class_name__iexact=str(class_name).strip(),
                section__iexact=str(section).strip()
            ).exists():
                skipped += 1
                continue

            Student.objects.create(
                school=school,
                name=str(name).strip(),
                class_name=str(class_name).strip(),
                section=str(section).strip()
            )
            created += 1

        messages.success(
            request,
            f"Students imported successfully ✅ | Added: {created} | Skipped: {skipped}"
        )

        # 👇 UX decision: stay on import page
        return redirect("students:import_students")

    # ✅ Clean GET request
    return render(request, "students/import_students.html")
