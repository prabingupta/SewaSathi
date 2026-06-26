from django.conf import settings
from django.db import models
from services.models import ServiceCategory


class ServiceProvider(models.Model):
    """
    Extended profile for users with role = PROVIDER.
    One-to-one with User: every provider has exactly one profile,
    and every profile belongs to exactly one user.
    """

    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='provider_profile'
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='providers'
    )
    bio = models.TextField(
        max_length=1000,
        blank=True,
        help_text="Short description of skills and experience"
    )
    experience_years = models.PositiveSmallIntegerField(default=0)
    hourly_rate = models.DecimalField(
        max_digits=8, decimal_places=2,
        null=True, blank=True,
        help_text="Approximate rate in NPR per hour/visit"
    )
    service_area = models.CharField(
        max_length=255,
        blank=True,
        help_text="e.g. Kathmandu, Pokhara, Lalitpur"
    )
    citizenship_or_license = models.FileField(
        upload_to='provider_documents/',
        blank=True, null=True,
        help_text="Citizenship or license document for verification"
    )
    verification_status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING
    )
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"

    @property
    def average_rating(self):
        from django.db.models import Avg
        result = self.bookings_received.filter(
            review__isnull=False
        ).aggregate(avg=Avg('review__rating'))
        return round(result['avg'], 1) if result['avg'] else None

    @property
    def review_count(self):
        return self.bookings_received.filter(review__isnull=False).count()
