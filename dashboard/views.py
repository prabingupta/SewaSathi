import json
from datetime import timedelta
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum
from django.utils import timezone
from django.shortcuts import render
from accounts.models import User
from bookings.models import Booking
from providers.models import ServiceProvider
from services.models import ServiceCategory


@staff_member_required
def admin_dashboard_view(request):
    total_users = User.objects.filter(role=User.Role.CUSTOMER).count()
    total_providers = ServiceProvider.objects.count()
    verified_providers = ServiceProvider.objects.filter(
        verification_status=ServiceProvider.VerificationStatus.VERIFIED
    ).count()
    total_bookings = Booking.objects.count()

    bookings_by_status = list(
        Booking.objects.values('status').annotate(count=Count('id')).order_by('status')
    )
    status_labels = [b['status'] for b in bookings_by_status]
    status_counts = [b['count'] for b in bookings_by_status]

    revenue_estimate = Booking.objects.filter(
        status=Booking.Status.COMPLETED
    ).aggregate(total=Sum('provider__hourly_rate'))['total'] or 0

    top_categories = list(
        ServiceCategory.objects.annotate(
            provider_count=Count('providers')
        ).order_by('-provider_count')[:5]
    )
    category_labels = [c.name for c in top_categories]
    category_counts = [c.provider_count for c in top_categories]

    thirty_days_ago = timezone.now() - timedelta(days=30)
    recent_signups = User.objects.filter(
        date_joined__gte=thirty_days_ago
    ).order_by('-date_joined')[:8]

    context = {
        'total_users': total_users,
        'total_providers': total_providers,
        'verified_providers': verified_providers,
        'total_bookings': total_bookings,
        'revenue_estimate': revenue_estimate,
        'recent_signups': recent_signups,
        'status_labels_json': json.dumps(status_labels),
        'status_counts_json': json.dumps(status_counts),
        'category_labels_json': json.dumps(category_labels),
        'category_counts_json': json.dumps(category_counts),
    }
    return render(request, 'dashboard/admin_dashboard.html', context)
