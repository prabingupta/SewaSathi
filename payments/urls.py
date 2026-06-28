from django.urls import path
from . import views

urlpatterns = [
    path('initiate/<int:booking_id>/', views.initiate_payment_view, name='initiate_payment'),
    path('callback/success/', views.payment_success_view, name='payment_success'),
    path('callback/failure/', views.payment_failure_view, name='payment_failure'),
]
