from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.http import HttpResponse

def create_admin(request):
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse("Admin already exists")

    User.objects.create_superuser(
        username="admin",
        password="Admin@123",
        email="admin@school.com"
    )
    return HttpResponse("Admin created successfully")

def post_login_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("/login/")

    if user.is_superuser:
        return redirect("/admin/")

    if user.groups.filter(name="Teacher").exists():
        return redirect("/attendance/class-wise/")

    if user.groups.filter(name="Accountant").exists():
        return redirect("/fees/defaulters/")

    return redirect("/")
