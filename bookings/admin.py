from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'customer', 'provider', 'preferred_date',
        'preferred_time_slot', 'status', 'created_at'
    )
    list_filter = ('status', 'preferred_time_slot')
    search_fields = ('customer__username', 'provider__user__username', 'address')
    autocomplete_fields = ('customer', 'provider')
    readonly_fields = ('created_at', 'updated_at')
