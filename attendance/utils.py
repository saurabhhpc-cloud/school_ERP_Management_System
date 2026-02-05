from datetime import date
from calendar import monthrange

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
        is_present=True
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
