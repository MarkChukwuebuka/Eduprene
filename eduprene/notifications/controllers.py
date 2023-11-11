import os

from django.core.mail import send_mail, BadHeaderError
from .services import register_notification_service
from constants.other_constants import NOTIFICATION_CHANNELS, GENERAL_STATUS


def email_notification_handler(user, subject, message, event):
    # Send email to user
    try:
        mail = send_mail(
            subject=subject,
            recipient_list=[user.email],
            message=message,
            from_email=os.getenv('DEFAULT_FROM_EMAIL'),
            html_message=message
        )

        # Register in Notification Model
        data = {
            "email": user.email,
            "subject": subject,
            "message": message,
            "status": GENERAL_STATUS['SUCCESS'] if mail == 1 else GENERAL_STATUS['FAILED']
        }
        register_notification_service(user, NOTIFICATION_CHANNELS['EMAIL'], event, data)

        return mail

    except Exception as e:
        return False
