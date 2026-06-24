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
