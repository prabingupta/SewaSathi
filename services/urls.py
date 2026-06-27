from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_services_view, name='manage_services'),
    path('delete/<int:pk>/', views.delete_service_view, name='delete_service'),
]
