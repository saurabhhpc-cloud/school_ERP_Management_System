from django.urls import path
from . import views
from .admin_views import load_subjects

app_name = "exams"

urlpatterns = [
    path("", views.exam_list, name="list"), 
    path("ajax/load-subjects/", load_subjects, name="ajax_load_subjects"),
]
