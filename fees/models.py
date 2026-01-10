from django.db import models
from students.models import Student

class FeeStructure(models.Model):
    class_name = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Class {self.class_name} - ₹{self.amount}"


class StudentFee(models.Model):
    STATUS_CHOICES = (
        ("Paid", "Paid"),
        ("Due", "Due"),
        ("Partial", "Partial"),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Due")
    due_date = models.DateField()

    @property
    def due_amount(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"{self.student.full_name} - {self.status}"
    
