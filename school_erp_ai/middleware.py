from django.shortcuts import redirect
from django.urls import reverse

class RoleRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            path = request.path

            # 🚫 Non-staff trying to access admin
            if path.startswith("/admin") and not request.user.is_staff:
                if request.user.groups.filter(name="Teacher").exists():
                    return redirect("/teacher/dashboard/")
                if request.user.groups.filter(name="Parent").exists():
                    return redirect("/dashboard/")
                return redirect("/login/")

        return self.get_response(request)
