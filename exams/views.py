from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Exam


@login_required
def exam_list(request):
    exams = Exam.objects.all().order_by("-id")

    context = {
        "exams": exams,
        "total_exams": exams.count()
    }

    return render(request, "exams/exam_list.html", context)
