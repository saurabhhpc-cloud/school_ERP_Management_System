from datetime import date
from calendar import monthrange
from admission.models import StudentProfile
from django.db.models import Count, Q
from .models import Attendance, AttendanceSummary


def generate_monthly_attendance_summary(school, year, month):
    """
    Calculate monthly attendance percentage for a school
    """

    start_date = date(year, month, 1)
    end_date = date(year, month, monthrange(year, month)[1])

    total_records = Attendance.objects.filter(
        school=school,
        date__range=(start_date, end_date)
    ).count()

    present_records = Attendance.objects.filter(
        school=school,
        date__range=(start_date, end_date),
        status="P"
    ).count()

    percentage = 0
    if total_records > 0:
        percentage = round((present_records / total_records) * 100, 2)

    AttendanceSummary.objects.update_or_create(
        school=school,
        month=start_date,
        defaults={"percentage": percentage}
    )

    return percentage

def get_attendance_eligible_students(class_name, academic_year):
    return StudentProfile.objects.filter(
        is_active=True,
        roll_number__isnull=False,
        admission__class_applied=class_name,
        admission__academic_year=academic_year,
        admission__admission_status="CONFIRMED",
    ).select_related("admission", "parent").order_by("roll_number")
