from .models import StudentProfile, Admission

def generate_roll_number(admission):
    """
    Generates next roll number class + academic year wise
    """

    same_class_students = StudentProfile.objects.filter(
        admission__academic_year=admission.academic_year,
        admission__class_applied=admission.class_applied,
        is_active=True,
        roll_number__isnull=False
    )

    last_roll = same_class_students.order_by("-roll_number").first()

    if last_roll:
        return last_roll.roll_number + 1

    return 1
