from django.http import JsonResponse
from .models import Exam, Subject

def load_subjects(request):
    exam_id = request.GET.get('exam_id')

    subjects = []
    if exam_id:
        try:
            exam = Exam.objects.get(id=exam_id)
            subjects = Subject.objects.filter(
                class_name=exam.class_name
            ).values('id', 'name')
        except Exam.DoesNotExist:
            pass

    return JsonResponse(list(subjects), safe=False)

