from django.urls import path
from . import views

urlpatterns = [
    path('write/<int:booking_pk>/', views.write_review_view, name='write_review'),
]
