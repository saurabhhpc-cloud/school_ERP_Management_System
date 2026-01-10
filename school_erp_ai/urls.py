"""
URL configuration for school_erp_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import post_login_redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .views import create_admin

def create_admin(request):
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser(
            username="admin",
            password="Admin@123",
            email="admin@school.com"
        )
        return HttpResponse("✅ Admin created")
    return HttpResponse("⚠ Admin already exists")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", include("django.contrib.auth.urls")),

    # 👇 ADD THIS LINE
    path("create-admin/", create_admin, name="create_admin"),

    path("", include("attendance.urls")),
    path("attendance/", include("attendance.urls")),
    path("fees/", include("fees.urls")),
    path("leads/", include("leads.urls")),
]