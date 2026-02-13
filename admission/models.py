from django.db import models
from django.contrib.auth.models import User
from schools.models import School


# -------------------------
# Choices
# -------------------------

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
)

ADMISSION_TYPE = (
    ("NEW", "New Admission"),
    ("TRANSFER", "Transfer"),
)

ADMISSION_STATUS = (
    ("ENQUIRY", "Enquiry"),
    ("APPLIED", "Applied"),
    ("CONFIRMED", "Confirmed"),
    ("REJECTED", "Rejected"),
)

PAYMENT_MODE = (
    ("CASH", "Cash"),
    ("ONLINE", "Online"),
    ("CHEQUE", "Cheque"),
)

# -------------------------
# Parent / Guardian
# -------------------------

class ParentProfile(models.Model):
    father_name = models.CharField(max_length=100)
    mother_name = models.CharField(max_length=100, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)

    primary_mobile = models.CharField(max_length=15, unique=True)
    alternate_mobile = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)

    def __str__(self):
        return self.father_name


# -------------------------
# Student Core Profile
# -------------------------

class StudentProfile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    roll_number = models.PositiveIntegerField(null=True, blank=True)
    student_photo = models.ImageField(upload_to="students/photos/", blank=True)
    aadhaar_no = models.CharField(max_length=12, blank=True)

    parent = models.ForeignKey(
        ParentProfile,
        on_delete=models.CASCADE,
        related_name="children"
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name="admissions"
    )
    is_active = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# -------------------------
# Admission Record
# -------------------------

class Admission(models.Model):
    student = models.OneToOneField(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name="admission"
    )

    academic_year = models.CharField(max_length=20)
    class_applied = models.CharField(max_length=10)
    section = models.CharField(max_length=5, blank=True)

    admission_type = models.CharField(
        max_length=10,
        choices=ADMISSION_TYPE
    )

    admission_date = models.DateField(auto_now_add=True)

    admission_status = models.CharField(
        max_length=15,
        choices=ADMISSION_STATUS,
        default="ENQUIRY"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True)
    admission_no = models.CharField(max_length=30, unique=True, blank=True)
    def __str__(self):
        return f"{self.student} - {self.academic_year}"


# -------------------------
# Previous School (Optional)
# -------------------------

class PreviousSchool(models.Model):
    admission = models.OneToOneField(
        Admission,
        on_delete=models.CASCADE,
        related_name="previous_school"
    )

    school_name = models.CharField(max_length=200, blank=True)
    board = models.CharField(max_length=50, blank=True)
    last_class = models.CharField(max_length=20, blank=True)
    tc_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.school_name


# -------------------------
# Documents (Dynamic)
# -------------------------

class AdmissionDocument(models.Model):
    admission = models.ForeignKey(
        Admission,
        on_delete=models.CASCADE,
        related_name="documents"
    )

    document_type = models.CharField(max_length=100)
    document_file = models.FileField(upload_to="admission/documents/", blank=True)
    is_submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.document_type


# -------------------------
# Fees
# -------------------------

class AdmissionFee(models.Model):
    admission = models.OneToOneField(
        Admission,
        on_delete=models.CASCADE,
        related_name="fees"
    )

    admission_fee = models.DecimalField(max_digits=10, decimal_places=2)
    tuition_fee = models.DecimalField(max_digits=10, decimal_places=2)

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE
    )

    def __str__(self):
        return f"Fees - {self.admission.student}"

# Create your models here.
