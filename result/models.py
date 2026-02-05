from django.db import models
from django.utils.html import format_html
from students.models import Student

class Result(models.Model):
    school = models.ForeignKey(
        "schools.School",
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(
        "exams.Subject",
        on_delete=models.CASCADE
    )
    exam = models.ForeignKey(
        "exams.Exam",
        on_delete=models.CASCADE
    )

    marks_obtained = models.FloatField()
    max_marks = models.FloatField(default=100)

    def save(self, *args, **kwargs):
        percent = (self.marks_obtained / self.max_marks) * 100

        if percent >= 75:
            self.grade = "A"
        elif percent >= 60:
            self.grade = "B"
        elif percent >= 40:
            self.grade = "C"
        else:
            self.grade = "F"

        self.status = "PASS" if percent >= 40 else "FAIL"
        super().save(*args, **kwargs)

    # 🔹 Admin UI badge
    def status_badge(self):
        if self.status == 'PASS':
            return format_html(
                '<span style="color:green;font-weight:bold;">PASS</span>'
            )
        return format_html(
            '<span style="color:red;font-weight:bold;">FAIL</span>'
        )

    status_badge.short_description = "Status"

    def __str__(self):
        return f"{self.student} - {self.subject} ({self.exam})"

