import logging
import os
from django.core.mail import send_mail
from .services import register_notification_service
from constants.other_constants import NOTIFICATION_CHANNELS, GENERAL_STATUS


class EmailService:
    @staticmethod
    def email_notification_handler(email, subject, message):
        mail = None
        error = None

        # Send email to user
        try:
            mail = send_mail(
                subject=subject,
                recipient_list=[email],
                message="",
                from_email=os.getenv('DEFAULT_FROM_EMAIL'),
                html_message=message
            )

            return mail, error

        except Exception as e:
            error = e
            logging.error(e)
            return mail, error
