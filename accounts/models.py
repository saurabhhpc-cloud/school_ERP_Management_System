from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    is_parent = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.is_admin = True
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def role(self):
        if self.is_admin:
            return "Admin"
        if self.is_teacher:
            return "Teacher"
        if self.is_parent:
            return "Parent"
        return "User"
