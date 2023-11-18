import logging
from celery import shared_task

from .controllers import EmailService
from .services import register_notification_service
from constants.other_constants import NOTIFICATION_CHANNELS, GENERAL_STATUS

logger = logging.getLogger(__name__)

@shared_task
def email_queue(email, subject, message, event):
    try:
        mail, error = EmailService.email_notification_handler(email, subject, message)

        # Register in Notification Model
        data = {
            "email": email,
            "subject": subject,
            "message": message,
            "status": GENERAL_STATUS['SUCCESS'] if mail == 1 else GENERAL_STATUS['FAILED'],
            "error": error
        }
        register_notification_queue(email, NOTIFICATION_CHANNELS['EMAIL'], event, data)

        return mail

    except Exception as e:
        logger.exception("An error occured in celery: ", str(e))


@shared_task
def register_notification_queue(email, channel, event, data=None):
    register_notification_service(email, channel, event, data)
