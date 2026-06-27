from django.db import models


class ServiceCategory(models.Model):
    """
    Admin-managed service categories, e.g. Electrician, Plumber, Painter.
    Matches doc Module 3: Admin can Add/Update/Delete categories.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.CharField(max_length=255, blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Optional: a short label/emoji/icon code for UI display"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Service(models.Model):
    """
    A specific offering a provider lists under their category, with its own price.
    e.g. Provider 'Samir' (Electrician) offers:
      - "Fan Installation" - Rs 300
      - "Wiring Repair" - Rs 500
    Matches doc database design: Service table (provider_id, category_id, price).
    """
    provider = models.ForeignKey(
        'providers.ServiceProvider',
        on_delete=models.CASCADE,
        related_name='services'
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name='services'
    )
    name = models.CharField(max_length=150, help_text="e.g. 'Fan Installation', 'Pipe Leak Repair'")
    description = models.CharField(max_length=255, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - Rs.{self.price} ({self.provider.user.username})"
