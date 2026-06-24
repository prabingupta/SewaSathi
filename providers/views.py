from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User
from .forms import ServiceProviderForm
from .models import ServiceProvider


@login_required
def complete_profile_view(request):
    if request.user.role != User.Role.PROVIDER:
        messages.error(request, "Only service providers can access this page.")
        return redirect('home')

    if hasattr(request.user, 'provider_profile'):
        return redirect('provider_my_profile')

    if request.method == 'POST':
        form = ServiceProviderForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(
                request,
                "Profile submitted! Your account is pending verification by our team."
            )
            return redirect('provider_my_profile')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ServiceProviderForm()

    return render(request, 'providers/complete_profile.html', {'form': form})


@login_required
def my_profile_view(request):
    profile = get_object_or_404(ServiceProvider, user=request.user)
    return render(request, 'providers/my_profile.html', {'profile': profile})
