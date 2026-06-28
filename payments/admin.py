from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'transaction_uuid', 'amount', 'status', 'esewa_ref_id', 'created_at')
    list_filter = ('status',)
    search_fields = ('transaction_uuid', 'esewa_ref_id', 'booking__customer__username')
    readonly_fields = ('created_at', 'updated_at')
