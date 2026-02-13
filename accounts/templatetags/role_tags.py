from django import template

register = template.Library()

@register.filter
def has_role(user, role_name):
    return user.groups.filter(name__iexact=role_name).exists()
