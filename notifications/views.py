from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Notification


@login_required
def notifications_list_view(request):
    notifications = Notification.objects.filter(recipient=request.user)
    notifications.filter(is_read=False).update(is_read=True)
    return render(request, 'notifications/list.html', {'notifications': notifications})


@login_required
def mark_read_and_redirect_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect(notification.link or 'home')
