from django.db import models

class Lead(models.Model):
    SOURCE_CHOICES = (
        ("Home", "Home Page"),
        ("Popup", "Popup"),
        ("Fees", "Fees Page"),
        ("Attendance", "Attendance Page"),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=15)
    institute = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50, blank=True)

    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default="Home"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.source}"
