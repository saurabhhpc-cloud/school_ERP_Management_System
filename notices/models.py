from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Notice(models.Model):
    send_to_students = models.BooleanField(default=False)
    send_to_teachers = models.BooleanField(default=False)
    send_to_parents = models.BooleanField(default=False)

    class_name = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="Fill only if class-specific notice for students"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    publish_date = models.DateField()
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # ❗ At least one audience must be selected
        if not (self.send_to_students or self.send_to_teachers or self.send_to_parents):
            raise ValidationError(
                "Select at least one audience (students / teachers / parents)."
            )

        # ❗ Class name only allowed for students
        if self.class_name and not self.send_to_students:
            raise ValidationError(
                "Class name can be used only when sending notice to students."
            )

    def __str__(self):
        return self.title

