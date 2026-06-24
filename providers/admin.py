from django.contrib import admin
from .models import ServiceProvider


@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'category', 'experience_years',
        'hourly_rate', 'verification_status', 'is_available', 'created_at'
    )
    list_filter = ('verification_status', 'category', 'is_available')
    search_fields = ('user__username', 'user__email', 'service_area')
    list_editable = ('verification_status',)
    autocomplete_fields = ('user',)

    fieldsets = (
        ('Provider', {
            'fields': ('user', 'category', 'bio', 'experience_years')
        }),
        ('Pricing & Location', {
            'fields': ('hourly_rate', 'service_area')
        }),
        ('Verification', {
            'fields': ('verification_status', 'citizenship_or_license', 'is_available')
        }),
    )
