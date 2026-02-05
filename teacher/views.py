from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .models import Teacher
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TeacherForm
from attendance.models import Attendance


from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils import timezone
from attendance.models import Attendance
from students.models import Student
from .models import Teacher


def is_teacher(user):
    return user.groups.filter(name="Teacher").exists() or user.is_superuser


@login_required
@user_passes_test(is_teacher)
def teacher_dashboard(request):
    teacher = Teacher.objects.get(user=request.user)
    today = timezone.now().date()

    students = Student.objects.filter(
        class_name=teacher.class_name,
        section=teacher.section,
        school=request.user.school
    )

    total_students = students.count()

    present = Attendance.objects.filter(
        student__in=students,
        date=today,
        is_present=True
    ).count()

    absent = total_students - present
    percent = round((present / total_students) * 100, 2) if total_students else 0

    return render(
        request,
        "teacher/teacher_dashboard.html",
        {
            "total_students": total_students,
            "present": present,
            "absent": absent,
            "percent": percent,
            "teacher": teacher
        }
    )
@login_required
def teacher_list(request):
    query = request.GET.get("subject")

    teacher = Teacher.objects.all()
    if query:
        teacher = teacher.filter(subject__icontains=query)

    return render(
        request,
        "teacher/teacher_list.html",
        {"teacher": teacher}
    )

@login_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect("teachers:list")
    else:
        form = TeacherForm(instance=teacher)

    return render(request, "teacher/teacher_form.html", {"form": form})


@login_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect("teachers:list")


@login_required
def teacher_attendance(request, teacher_id):
    records = Attendance.objects.filter(
    student__teacher__id=teacher_id)

    return render(
        request,
        "teacher/teacher_attendance.html",
        {"records": records}
    )

@login_required
def mark_attendance(request):
    # 🔐 Sirf Teacher allow
    if not request.user.groups.filter(name="Teacher").exists():
        return redirect("schools:dashboard")

    teacher = Teacher.objects.get(user=request.user)
    today = timezone.now().date()

    students = Student.objects.filter(
        class_name=teacher.class_name,
        section=teacher.section
    )

    if request.method == "POST":
        for student in students:
            status = request.POST.get(str(student.id))  # "P" or "A"
            Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={
                    "school": teacher.user.school,
                    "teacher": teacher,
                    "is_present": status == "P"
                }
            )
        return redirect("teachers:attendance")

    return render(
        request,
        "teacher/mark_attendance.html",
        {
            "students": students,
            "today": today
        }
    )