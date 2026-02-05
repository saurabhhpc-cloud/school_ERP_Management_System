from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    class_name = models.CharField(max_length=10)
    section = models.CharField(max_length=5)

    def __str__(self):
        return self.user.username

class Student(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )