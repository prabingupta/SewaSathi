from django.db import models
from bookings.models import Booking


class Payment(models.Model):
    """
    Tracks a payment attempt for a booking via eSewa.
    Matches doc Module 8: Payment System (online payment, payment history).
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'

    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='payment'
    )
    transaction_uuid = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    esewa_ref_id = models.CharField(max_length=100, blank=True, help_text="eSewa's transaction reference, once confirmed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment #{self.pk} - Booking #{self.booking_id} - {self.status}"
