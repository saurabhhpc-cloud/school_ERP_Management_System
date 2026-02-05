from django.db import models
from schools.models import School
from students.models import Student
from teacher.models import Teacher


class Attendance(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ("student", "date")
        verbose_name_plural = "Student Attendance"

    def __str__(self):
        return f"{self.student} - {self.date}"

class AttendanceSummary(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    month = models.DateField()
    percentage = models.FloatField()

    class Meta:
        unique_together = ("school", "month")
        verbose_name_plural = "Attendance Summary"

    def __str__(self):
        return f"{self.school} - {self.month.strftime('%b %Y')}"
    