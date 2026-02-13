from django.urls import path
from . import views

app_name = "admission"

urlpatterns = [
    path("", views.admission_list, name="list"),
    path("enquiry/new/", views.create_enquiry, name="create_enquiry"),

    path("<int:admission_id>/", views.admission_detail, name="detail"),

    path("<int:admission_id>/apply/", views.mark_applied, name="mark_applied"),
    path("<int:admission_id>/confirm/", views.confirm_admission, name="confirm"),
    path("<int:admission_id>/reject/", views.reject_admission, name="reject"),
    
]
