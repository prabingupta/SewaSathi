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
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
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

    def recommendation_score(self, max_price=1000):
        """
        Weighted scoring algorithm ranking providers by rating, review volume,
        experience, and price. Each factor is normalized to 0-1, then combined
        with fixed weights. This is a transparent, explainable heuristic --
        not a trained ML model -- chosen because we don't yet have enough
        booking volume for a real model to learn meaningful patterns from.

        Weights (sum to 1.0):
          - Rating quality:    40%
          - Review confidence: 20% (rewards proven track record over a single lucky review)
          - Experience:        20% (diminishing returns past ~10 years)
          - Affordability:     20% (lower price scores higher, capped at max_price)
        """
        rating = self.average_rating or 0
        rating_score = rating / 5.0

        review_count = self.review_count
        confidence_score = min(review_count / 10.0, 1.0)

        experience_score = min(self.experience_years / 10.0, 1.0)

        if self.hourly_rate and self.hourly_rate > 0:
            price_score = max(0, 1 - (float(self.hourly_rate) / max_price))
        else:
            price_score = 0.5

        return (
            rating_score * 0.40 +
            confidence_score * 0.20 +
            experience_score * 0.20 +
            price_score * 0.20
        )
