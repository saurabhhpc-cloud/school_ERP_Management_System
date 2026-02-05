from django.core.management.base import BaseCommand
from schools.models import School
from attendance.utils import generate_monthly_attendance_summary
from datetime import date


class Command(BaseCommand):
    help = "Generate monthly attendance summary for all schools"

    def handle(self, *args, **kwargs):
        today = date.today()
        year = today.year
        month = today.month

        for school in School.objects.all():
            generate_monthly_attendance_summary(school, year, month)

        self.stdout.write(self.style.SUCCESS("Attendance summary generated"))
