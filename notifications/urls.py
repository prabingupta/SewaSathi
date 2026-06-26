from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications_list_view, name='notifications_list'),
    path('go/<int:pk>/', views.mark_read_and_redirect_view, name='notification_redirect'),
]
