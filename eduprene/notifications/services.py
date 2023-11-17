import logging

from .models import Notification


def register_notification_service(email, channel, event, data=None):
    if data is None:
        data = {}

    try:
        new_notification = Notification.objects.create(email=email, channel=channel, event=event, data=data)
        return True

    except Exception as e:
        logging.error(e)
        return False