from django.db import models
from django.conf import settings
from .middleware import get_current_school

class School(models.Model):
    name = models.CharField(max_length=255)
    board = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SchoolBaseModel(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        editable=False
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.school:
            school = get_current_school()
            if not school:
                raise ValueError("School context not available")
            self.school = school
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    school = models.ForeignKey(
        School,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.school}"
