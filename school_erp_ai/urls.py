from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from school_erp_ai.admin_site import admin_site
from accounts.views import user_login
from parents.views import parent_dashboard
from django.contrib.auth import views as auth_views


def root_redirect(request):
    return redirect("login")


urlpatterns = [
    # Auth
    path("login/", user_login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Parent Dashboard
    path("parents/dashboard/", parent_dashboard, name="parent-dashboard"),

    # School Admin Dashboard
    path("schools/", include("schools.urls")),

    # Custom Admin (ONLY ONE)
    path("admin/", admin_site.urls),

    # Apps
    path("accounts/", include("accounts.urls")),
    path("parents/", include("parents.urls")),
    path("students/", include("students.urls")),
    path("fees/", include("fees.urls")),
    path("attendance/",include(("attendance.urls", "attendance"), namespace="attendance")),
    path("leads/", include("leads.urls")),
    path("exams/", include("exams.urls")),
    path("teacher/", include(("teacher.urls", "teachers"), namespace="teachers")),

    # Root
    path("", root_redirect),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
