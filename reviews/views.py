from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from bookings.models import Booking
from .forms import ReviewForm


@login_required
def write_review_view(request, booking_pk):
    booking = get_object_or_404(
        Booking, pk=booking_pk, customer=request.user,
        status=Booking.Status.COMPLETED
    )

    if hasattr(booking, 'review'):
        messages.info(request, "You've already reviewed this booking.")
        return redirect('customer_bookings')

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.booking = booking
            review.customer = request.user
            review.save()
            messages.success(request, "Thanks for your feedback!")
            return redirect('customer_bookings')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ReviewForm()

    return render(request, 'reviews/write_review.html', {
        'form': form, 'booking': booking
    })
