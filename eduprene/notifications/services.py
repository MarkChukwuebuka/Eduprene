from .models import Notification


def register_notification_service(user, channel, event, data=None):
    if data is None:
        data = {}

    try:
        new_notification = Notification.objects.create(user, channel, event, data)
        new_notification.save()

        return True

    except Exception as e:
        return False