from django.db import models
from schools.models import School
from teacher.models import Teacher
from admission.models import StudentProfile

ATTENDANCE_STATUS = (
    ("P", "Present"),
    ("A", "Absent"),
)

class Attendance(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="attendance_records"
    )

    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    date = models.DateField()

    status = models.CharField(
        max_length=1,
        choices=ATTENDANCE_STATUS
    )

    class Meta:
        unique_together = ("student", "date")
        ordering = ["-date"]
        verbose_name_plural = "Student Attendance"

    def __str__(self):
        return f"{self.student} - {self.date}"
