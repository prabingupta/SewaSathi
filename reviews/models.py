from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from bookings.models import Booking


class Review(models.Model):
    """
    A customer's rating + feedback for a completed booking.
    One review per booking, matches doc Module 9: Reviews & Ratings.
    """
    booking = models.OneToOneField(
        Booking,
        on_delete=models.CASCADE,
        related_name='review'
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.rating}★ by {self.customer.username} for booking #{self.booking.pk}"
