def get_redirect_url(user):
    if user.is_parent:
        return "/dashboard/"
    if user.is_teacher:
        return "/teacher/dashboard/"
    if user.is_admin:
        return "/admin/"
    return "/"