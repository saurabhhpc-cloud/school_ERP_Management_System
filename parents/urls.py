from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "parents"

urlpatterns = [
    path("dashboard/", views.parent_dashboard, name="parent_dashboard"),
    path("fees/<int:student_id>/", views.parent_fees, name="parent_fees"),
    path("login/", auth_views.LoginView.as_view(template_name="parents/login.html"), name="login"),
    path("logout/", views.parent_logout, name="logout"),
]