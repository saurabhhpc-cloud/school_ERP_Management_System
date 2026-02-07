from django.db import models
from schools.models import School
from admission.models import StudentProfile


class FeeStructure(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="fee_structures"
    )

    class_name = models.CharField(max_length=20)
    fee_type = models.CharField(max_length=50, default="Tuition")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.class_name} - {self.fee_type}"
    
class FeePayment(models.Model):
    STATUS_CHOICES = (
        ("paid", "Paid"),
        ("pending", "Pending"),
    )

    PAYMENT_MODE = (
        ("Cash", "Cash"),
        ("Online", "Online"),
    )

    school = models.ForeignKey(School, on_delete=models.CASCADE)
    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        null=True,      
        blank=True,
        related_name="fee_payments"
    )

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_mode = models.CharField(max_length=50)
    status = models.CharField(max_length=20)  # paid / pending
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Fees Management"
    def __str__(self):
        return f"{self.student} - {self.amount_paid}"
