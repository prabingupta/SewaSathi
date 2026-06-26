from .models import Notification


def notify(recipient, notification_type, message, link=''):
    """
    Single entry point for creating notifications.
    Keeping this in one place means every part of the app that needs
    to notify a user calls the same function, instead of duplicating
    Notification.objects.create(...) everywhere.
    """
    return Notification.objects.create(
        recipient=recipient,
        notification_type=notification_type,
        message=message,
        link=link
    )
