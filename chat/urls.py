from django.urls import path
from . import views

urlpatterns = [
    path('<int:booking_id>/', views.chat_room_view, name='chat_room'),
]
