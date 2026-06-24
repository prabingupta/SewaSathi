from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:provider_pk>/', views.create_booking_view, name='create_booking'),
    path('my-bookings/', views.customer_bookings_view, name='customer_bookings'),
    path('cancel/<int:pk>/', views.cancel_booking_view, name='cancel_booking'),
    path('provider/incoming/', views.provider_bookings_view, name='provider_bookings'),
    path('provider/update/<int:pk>/<str:new_status>/', views.update_booking_status_view, name='update_booking_status'),
]
