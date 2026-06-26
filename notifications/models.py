from django.conf import settings
from django.db import models


class Notification(models.Model):
    """
    In-app notification for a user, triggered by booking lifecycle events.
    Matches doc Module 11: Notifications.
    """

    class NotificationType(models.TextChoices):
        BOOKING_CREATED = 'BOOKING_CREATED', 'New Booking Request'
        BOOKING_ACCEPTED = 'BOOKING_ACCEPTED', 'Booking Accepted'
        BOOKING_REJECTED = 'BOOKING_REJECTED', 'Booking Rejected'
        BOOKING_IN_PROGRESS = 'BOOKING_IN_PROGRESS', 'Service Started'
        BOOKING_COMPLETED = 'BOOKING_COMPLETED', 'Service Completed'
        BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Booking Cancelled'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    notification_type = models.CharField(max_length=25, choices=NotificationType.choices)
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, help_text="Relative URL to navigate to on click")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient.username}: {self.message[:40]}"
