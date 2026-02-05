from django.conf import settings
from django.db import models

class Parent(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="parent_profile",
        limit_choices_to={"is_parent": True}
    )

    emergency_contact = models.CharField(max_length=15, blank=True)
    occupation = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username



