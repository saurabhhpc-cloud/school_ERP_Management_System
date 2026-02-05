from django.urls import path
from .admin_views import load_subjects

urlpatterns = [
    path('ajax/load-subjects/', load_subjects, name='ajax_load_subjects'),
]
