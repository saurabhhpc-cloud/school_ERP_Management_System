from django.db import models
from teacher.models import Teacher

class Student(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)

    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students"
    )

    def __str__(self):
        return self.name


   