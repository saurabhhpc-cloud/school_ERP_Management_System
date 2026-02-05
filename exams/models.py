from django.db import models


class Exam(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="exams"
    )
    class_name = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.class_name})"
class Subject(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="subjects"
    )
    name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.class_name})"

class Result(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE,
        related_name="results"
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE
    )
    exam = models.ForeignKey(
        "exams.Exam",
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        "exams.Subject",
        on_delete=models.CASCADE
    )
    marks_obtained = models.FloatField()
    max_marks = models.FloatField(default=100)
