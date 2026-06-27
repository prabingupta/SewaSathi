from django.urls import path
from . import views

urlpatterns = [
    path('complete-profile/', views.complete_profile_view, name='provider_complete_profile'),
    path('my-profile/', views.my_profile_view, name='provider_my_profile'),
    path('browse/', views.browse_providers_view, name='browse_providers'),
    path('set-location/', views.set_location_view, name='set_location'),
    path('<int:pk>/', views.provider_detail_view, name='provider_detail'),
]
