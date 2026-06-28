from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from bookings.models import Booking
from .models import Message


@login_required
def chat_room_view(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    is_customer = booking.customer_id == request.user.id
    is_provider = hasattr(request.user, 'provider_profile') and booking.provider_id == request.user.provider_profile.id

    if not (is_customer or is_provider):
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, "You don't have access to this conversation.")
        return redirect('home')

    messages_qs = Message.objects.filter(booking=booking).select_related('sender')

    other_party = booking.provider.user if is_customer else booking.customer

    return render(request, 'chat/chat_room.html', {
        'booking': booking,
        'messages_history': messages_qs,
        'other_party': other_party,
    })
