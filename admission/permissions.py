from django.core.exceptions import PermissionDenied

def is_frontdesk(user):
    return user.groups.filter(name="FrontDesk").exists()

def is_admin(user):
    return user.groups.filter(name="Admin").exists()

def is_principal(user):
    return user.groups.filter(name="Principal").exists()