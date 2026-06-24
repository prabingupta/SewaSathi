from django.urls import path
from . import views

urlpatterns = [
    path('complete-profile/', views.complete_profile_view, name='provider_complete_profile'),
    path('my-profile/', views.my_profile_view, name='provider_my_profile'),
]
