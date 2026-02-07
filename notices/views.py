from datetime import date
from django.db import models
from .models import Notice

def get_notices_for_user(user):

    today = date.today()

    # 🔐 ADMIN / SCHOOL
    if user.is_superuser:
        return Notice.objects.filter(
            is_active=True,
            publish_date__lte=today
        )

    # 👨‍🏫 TEACHER
    if user.groups.filter(name="Teacher").exists():
        return Notice.objects.filter(
            is_active=True,
            publish_date__lte=today,
            target__in=["ALL", "TEACHERS"]
        )

    # 🧑‍🎓 STUDENT
    if user.groups.filter(name="Student").exists():
        student = user.student
        class_key = f"{student.class_name}{student.section}"

        return Notice.objects.filter(
            is_active=True,
            publish_date__lte=today
        ).filter(
            models.Q(target="ALL") |
            models.Q(target="CLASS", class_name=class_key)
        )

    # 👨‍👩‍👧 PARENT  ✅ NEW
    if user.groups.filter(name="Parent").exists():
        parent = user.parent
        student = parent.student
        class_key = f"{student.class_name}{student.section}"

        return Notice.objects.filter(
            is_active=True,
            publish_date__lte=today
        ).filter(
            models.Q(target="ALL") |
            models.Q(target="CLASS", class_name=class_key)
        )

    return Notice.objects.none()
