from django.core.mail import send_mail
from django.conf import settings

def send_admin_email(lead):
    subject = "🚨 New Lead Received - School ERP"
    message = f"""
New Lead Details:

Name: {lead.name}
Phone: {lead.phone}
Email: {lead.email}
City: {lead.city}
Institute: {lead.institute}
Role: {lead.role}

Login to dashboard to follow up.
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [settings.ADMIN_EMAIL],
        fail_silently=True,
    )
def send_admin_whatsapp(lead):
    message = (
        f"📢 *New Lead Received*\n\n"
        f"👤 Name: {lead.name}\n"
        f"📞 Phone: {lead.phone}\n"
        f"🏫 Institute: {lead.institute}\n"
        f"📍 City: {lead.city}"
    )

    # ABHI PRINT (later API connect)
    print("WHATSAPP TO ADMIN:")
    print(message)
