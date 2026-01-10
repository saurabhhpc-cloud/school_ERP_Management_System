def fee_reminder_message(student_name, total, paid, due, due_date):
    return (
        f"Dear Parent,\n\n"
        f"This is a reminder for *{student_name}*.\n"
        f"Total Fee: ₹{total}\n"
        f"Paid: ₹{paid}\n"
        f"*Due: ₹{due}*\n"
        f"Due Date: {due_date}\n\n"
        f"Please clear the dues at the earliest.\n"
        f"- School ERP"
    )
