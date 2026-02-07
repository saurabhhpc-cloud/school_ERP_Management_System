import threading

_thread_locals = threading.local()


def get_current_school():
    return getattr(_thread_locals, "school", None)


class SchoolContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not hasattr(request, "user"):
            return self.get_response(request)

        if (
            request.user.is_authenticated
            and hasattr(request.user, "userprofile")
            and request.user.userprofile.school
        ):
            _thread_locals.school = request.user.userprofile.school
        else:
            _thread_locals.school = None

        response = self.get_response(request)
        return response

