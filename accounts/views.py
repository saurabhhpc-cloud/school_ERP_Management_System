from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # ✅ ROLE BASED REDIRECT
            return redirect("post-login")

        else:
            return render(
                request,
                "accounts/login.html",
                {"error": "Invalid username or password"}
            )

    return render(request, "accounts/login.html")


@login_required
def post_login_redirect(request):
    user = request.user

    if user.groups.filter(name="Teacher").exists():
        return redirect("teachers:dashboard")

    if user.groups.filter(name="SchoolAdmin").exists() or user.is_superuser:
        return redirect("schools:dashboard")

    return redirect("parent-dashboard")
