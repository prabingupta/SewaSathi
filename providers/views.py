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


def browse_providers_view(request):
    from .models import ServiceProvider
    from services.models import ServiceCategory

    providers = ServiceProvider.objects.filter(
        verification_status=ServiceProvider.VerificationStatus.VERIFIED,
        is_available=True
    ).select_related('user', 'category')

    category_slug = request.GET.get('category')
    query = request.GET.get('q', '').strip()

    if category_slug:
        providers = providers.filter(category__slug=category_slug)

    if query:
        from django.db.models import Q
        providers = providers.filter(
            Q(user__username__icontains=query) |
            Q(bio__icontains=query) |
            Q(service_area__icontains=query) |
            Q(category__name__icontains=query)
        )

    categories = ServiceCategory.objects.filter(is_active=True)

    return render(request, 'providers/browse.html', {
        'providers': providers,
        'categories': categories,
        'selected_category': category_slug,
        'query': query,
    })


def provider_detail_view(request, pk):
    from django.shortcuts import get_object_or_404
    from .models import ServiceProvider

    provider = get_object_or_404(
        ServiceProvider.objects.select_related('user', 'category'),
        pk=pk,
        verification_status=ServiceProvider.VerificationStatus.VERIFIED
    )
    return render(request, 'providers/provider_detail.html', {'provider': provider})
