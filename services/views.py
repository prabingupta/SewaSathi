from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceForm
from .models import Service


@login_required
def manage_services_view(request):
    if not hasattr(request.user, 'provider_profile'):
        messages.error(request, "Only service providers can manage services.")
        return redirect('home')

    profile = request.user.provider_profile
    services = Service.objects.filter(provider=profile)

    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = profile
            service.category = profile.category
            service.save()
            messages.success(request, f"'{service.name}' added.")
            return redirect('manage_services')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = ServiceForm()

    return render(request, 'services/manage_services.html', {
        'form': form, 'services': services
    })


@login_required
def delete_service_view(request, pk):
    service = get_object_or_404(Service, pk=pk, provider=request.user.provider_profile)
    service.delete()
    messages.success(request, "Service removed.")
    return redirect('manage_services')
