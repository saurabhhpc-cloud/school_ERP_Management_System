from django.shortcuts import redirect

def post_login_redirect(request):
    user = request.user

    if not user.is_authenticated:
        return redirect("/login/")

    if user.is_superuser:
        return redirect("/admin/")

    if user.groups.filter(name="Teacher").exists():
        return redirect("/attendance/class-wise/")

    if user.groups.filter(name="Accountant").exists():
        return redirect("/fees/")

    return redirect("/login/")
