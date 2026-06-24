from django.conf import settings
from django.db import models
from providers.models import ServiceProvider


class Booking(models.Model):
    """
    A customer's request to hire a provider for a specific date/time window.
    Matches doc Module 4: Service Booking.
    """

    class TimeSlot(models.TextChoices):
        MORNING = 'MORNING', 'Morning (8am - 12pm)'
        AFTERNOON = 'AFTERNOON', 'Afternoon (12pm - 4pm)'
        EVENING = 'EVENING', 'Evening (4pm - 8pm)'

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        REJECTED = 'REJECTED', 'Rejected'

    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings_made'
    )
    provider = models.ForeignKey(
        ServiceProvider,
        on_delete=models.CASCADE,
        related_name='bookings_received'
    )
    preferred_date = models.DateField()
    preferred_time_slot = models.CharField(max_length=10, choices=TimeSlot.choices)
    address = models.CharField(max_length=255)
    notes = models.TextField(max_length=500, blank=True, help_text="Describe the issue or request")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.pk} - {self.customer.username} -> {self.provider.user.username}"

    @property
    def can_be_cancelled(self):
        return self.status not in [
            Booking.Status.COMPLETED,
            Booking.Status.CANCELLED,
            Booking.Status.REJECTED
        ]
