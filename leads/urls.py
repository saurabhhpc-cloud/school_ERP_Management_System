from django.urls import path
from . import views

app_name = "leads"

urlpatterns = [
    path("", views.leads_list, name="list"),
    path("create/", views.create_lead, name="create_lead"),
    path("dashboard/", views.leads_dashboard, name="leads_dashboard"),
]
