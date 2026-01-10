from django.db import models

class Student(models.Model):

    GENDER_CHOICES = (
        ("Male", "Male"),
        ("Female", "Female"),
    )

    full_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20, unique=True)
    class_name = models.CharField(max_length=20)
    section = models.CharField(max_length=5)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    parent_name = models.CharField(max_length=100)
    parent_mobile = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.class_name}-{self.section})"
