from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import *
from .permissions import is_frontdesk, is_admin, is_principal
from .utils import generate_roll_number


@login_required
def confirm_admission(request, admission_id):
    if not is_principal(request.user):
        raise PermissionDenied

    admission = get_object_or_404(Admission, id=admission_id)

    if admission.admission_status != "APPLIED":
        raise PermissionDenied("Admission not ready")

    # Generate Roll Number
    roll_no = generate_roll_number(admission)

    # Final lock
    admission.admission_status = "CONFIRMED"
    admission.save(update_fields=["admission_status"])

    student = admission.student
    student.roll_number = roll_no
    student.is_active = True
    student.save(update_fields=["roll_number", "is_active"])

    return redirect("admission:detail", admission_id)

@login_required
def mark_applied(request, admission_id):
    if not is_admin(request.user):
        raise PermissionDenied

    admission = Admission.objects.get(id=admission_id)

    if admission.admission_status != "ENQUIRY":
        raise Exception("Invalid state change")

    admission.admission_status = "APPLIED"
    admission.save()

    return redirect("admission:detail", admission_id)

@login_required
def create_enquiry(request):
    if not is_frontdesk(request.user):
        raise PermissionDenied

    if request.method == "POST":
        parent = ParentProfile.objects.create(
            father_name=request.POST["father_name"],
            primary_mobile=request.POST["mobile"]
        )

        student = StudentProfile.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            gender=request.POST["gender"],
            date_of_birth=request.POST["dob"],
            parent=parent
        )

        Admission.objects.create(
            student=student,
            academic_year=request.POST["academic_year"],
            class_applied=request.POST["class_applied"]
        )

        return redirect("admission:list")

    return render(request, "admission/enquiry_form.html")

@login_required
def reject_admission(request, admission_id):
    if not is_principal(request.user):
        raise PermissionDenied

    admission = Admission.objects.get(id=admission_id)
    admission.admission_status = "REJECTED"
    admission.save()

    return redirect("admission:list")

@login_required
def admission_list(request):
    admissions = Admission.objects.select_related(
        "student", "student__parent"
    ).order_by("-created_at")

    return render(
        request,
        "admission/list.html",
        {"admissions": admissions}
    )

@login_required
def admission_detail(request, admission_id):
    admission = get_object_or_404(
        Admission.objects.select_related("student", "student__parent"),
        id=admission_id
    )

    return render(
        request,
        "admission/detail.html",
        {"admission": admission}
    )