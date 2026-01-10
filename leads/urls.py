from django.urls import path
from .views import create_lead, leads_dashboard, home

urlpatterns = [
    path("", home, name="home"),
    path("lead/", create_lead, name="create_lead"),
    path("leads/dashboard/", leads_dashboard, name="leads_dashboard"),
]