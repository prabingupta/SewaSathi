from django.conf import settings
from django.db import models
from bookings.models import Booking


class Message(models.Model):
    """
    A chat message tied to a specific booking, between the customer and provider.
    Matches doc Module 7: Real-Time Chat (Customer <-> Provider, job discussion).
    """
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:40]}"
