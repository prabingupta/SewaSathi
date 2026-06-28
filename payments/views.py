import uuid
import base64
import json
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Booking
from .esewa import generate_signature, verify_signature
from .models import Payment


@login_required
def initiate_payment_view(request, booking_id):
    booking = get_object_or_404(
        Booking, pk=booking_id, customer=request.user,
        status=Booking.Status.COMPLETED
    )

    if hasattr(booking, 'payment') and booking.payment.status == Payment.Status.SUCCESS:
        messages.info(request, "This booking has already been paid for.")
        return redirect('customer_bookings')

    amount = booking.service.price if booking.service else (booking.provider.hourly_rate or 0)
    transaction_uuid = f"booking-{booking.pk}-{uuid.uuid4().hex[:8]}"

    payment, _ = Payment.objects.update_or_create(
        booking=booking,
        defaults={
            'transaction_uuid': transaction_uuid,
            'amount': amount,
            'status': Payment.Status.PENDING,
        }
    )

    signature = generate_signature(amount, transaction_uuid, settings.ESEWA_MERCHANT_CODE)

    context = {
        'amount': amount,
        'transaction_uuid': transaction_uuid,
        'product_code': settings.ESEWA_MERCHANT_CODE,
        'signature': signature,
        'form_url': settings.ESEWA_FORM_URL,
        'success_url': request.build_absolute_uri('/payments/callback/success/'),
        'failure_url': request.build_absolute_uri('/payments/callback/failure/'),
        'booking': booking,
    }
    return render(request, 'payments/initiate_payment.html', context)


def payment_success_view(request):
    encoded_data = request.GET.get('data', '')
    try:
        decoded = base64.b64decode(encoded_data).decode('utf-8')
        data = json.loads(decoded)
    except Exception:
        messages.error(request, "Invalid payment response.")
        return redirect('customer_bookings')

    signature = data.get('signature', '')
    signed_field_names = data.get('signed_field_names', '')

    if not verify_signature(data, signature, signed_field_names):
        messages.error(request, "Payment verification failed -- signature mismatch.")
        return redirect('customer_bookings')

    transaction_uuid = data.get('transaction_uuid')
    payment = get_object_or_404(Payment, transaction_uuid=transaction_uuid)

    if data.get('status') == 'COMPLETE':
        payment.status = Payment.Status.SUCCESS
        payment.esewa_ref_id = data.get('transaction_code', '')
        payment.save()
        messages.success(request, "Payment successful! Thank you.")
    else:
        payment.status = Payment.Status.FAILED
        payment.save()
        messages.error(request, "Payment was not completed.")

    return redirect('customer_bookings')


def payment_failure_view(request):
    messages.error(request, "Payment was cancelled or failed. You can try again.")
    return redirect('customer_bookings')
