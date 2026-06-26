from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from providers.models import ServiceProvider
from notifications.utils import notify
from .forms import BookingForm
from .models import Booking


@login_required
def create_booking_view(request, provider_pk):
    provider = get_object_or_404(
        ServiceProvider, pk=provider_pk,
        verification_status=ServiceProvider.VerificationStatus.VERIFIED
    )

    if request.user.role != User.Role.CUSTOMER:
        messages.error(request, "Only customers can book services.")
        return redirect('provider_detail', pk=provider_pk)

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.customer = request.user
            booking.provider = provider
            booking.save()

            notify(
                recipient=provider.user,
                notification_type='BOOKING_CREATED',
                message=f"New booking request from {request.user.username} for {booking.preferred_date}.",
                link='/bookings/provider/incoming/'
            )

            messages.success(request, f"Booking request sent to {provider.user.username}!")
            return redirect('customer_bookings')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = BookingForm(initial={'address': request.user.address})

    return render(request, 'bookings/create_booking.html', {
        'form': form, 'provider': provider
    })


@login_required
def customer_bookings_view(request):
    bookings = Booking.objects.filter(customer=request.user).select_related(
        'provider__user', 'provider__category'
    )
    return render(request, 'bookings/customer_bookings.html', {'bookings': bookings})


@login_required
def cancel_booking_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, customer=request.user)
    if booking.can_be_cancelled:
        booking.status = Booking.Status.CANCELLED
        booking.save()

        notify(
            recipient=booking.provider.user,
            notification_type='BOOKING_CANCELLED',
            message=f"{request.user.username} cancelled their booking for {booking.preferred_date}.",
            link='/bookings/provider/incoming/'
        )

        messages.success(request, "Booking cancelled.")
    else:
        messages.error(request, "This booking can no longer be cancelled.")
    return redirect('customer_bookings')


@login_required
def provider_bookings_view(request):
    if not hasattr(request.user, 'provider_profile'):
        messages.error(request, "Only service providers can view this page.")
        return redirect('home')

    bookings = Booking.objects.filter(
        provider=request.user.provider_profile
    ).select_related('customer')
    return render(request, 'bookings/provider_bookings.html', {'bookings': bookings})


@login_required
def update_booking_status_view(request, pk, new_status):
    booking = get_object_or_404(
        Booking, pk=pk, provider__user=request.user
    )
    valid_transitions = {
        'ACCEPTED': [Booking.Status.PENDING],
        'REJECTED': [Booking.Status.PENDING],
        'IN_PROGRESS': [Booking.Status.ACCEPTED],
        'COMPLETED': [Booking.Status.IN_PROGRESS],
    }

    notification_messages = {
        'ACCEPTED': f"Your booking with {request.user.username} was accepted!",
        'REJECTED': f"Your booking with {request.user.username} was rejected.",
        'IN_PROGRESS': f"{request.user.username} has started your service.",
        'COMPLETED': f"Your service with {request.user.username} is complete. Leave a review!",
    }

    if new_status in valid_transitions and booking.status in valid_transitions[new_status]:
        booking.status = new_status
        booking.save()

        notify(
            recipient=booking.customer,
            notification_type=f'BOOKING_{new_status}',
            message=notification_messages[new_status],
            link='/bookings/my-bookings/'
        )

        messages.success(request, f"Booking #{booking.pk} marked as {booking.get_status_display()}.")
    else:
        messages.error(request, "Invalid status change.")

    return redirect('provider_bookings')
