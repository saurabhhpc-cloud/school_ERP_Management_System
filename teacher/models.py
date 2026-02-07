from django.db import models
from django.conf import settings

class Teacher(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    class_name = models.CharField(max_length=10)
    section = models.CharField(max_length=5)
    subject = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username

