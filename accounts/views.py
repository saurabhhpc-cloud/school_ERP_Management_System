from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(request, username=username, password=password)
        print("AUTH RESULT:", user)

        if user:
            login(request, user)
            print("LOGIN SUCCESS, USER:", request.user)

            return redirect("/accounts/post-login/")  # 👈 TEMP DIRECT URL

        print("LOGIN FAILED")

    return render(request, "accounts/login.html")


@login_required
def post_login_redirect(request):
    user = request.user
    print("LOGGED USER =", user)

    if user.is_superuser:
        return redirect("schools:dashboard")

    if user.groups.filter(name="principal").exists():
        return redirect("schools:dashboard")

    if user.groups.filter(name="SchoolAdmin").exists():
        return redirect("schools:dashboard")

    if user.groups.filter(name="Teacher").exists():
        return redirect("teacher:dashboard")

    if user.groups.filter(name="Parent").exists():
        return redirect("parents:dashboard")

    logout(request)
    return redirect("accounts:login")
