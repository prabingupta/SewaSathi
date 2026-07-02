import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from bookings.models import Booking
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.booking_id = self.scope['url_route']['kwargs']['booking_id']
        self.room_group_name = f'chat_{self.booking_id}'
        user = self.scope['user']

        if not user.is_authenticated:
            await self.close()
            return

        is_allowed = await self.user_can_access_booking(user, self.booking_id)
        if not is_allowed:
            await self.close()
            return

        from channels.layers import get_channel_layer
        self.channel_layer_instance = get_channel_layer()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message'].strip()
        if not message_text:
            return

        user = self.scope['user']
        message = await self.save_message(user, self.booking_id, message_text)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_text,
                'sender': user.username,
                'sender_id': user.id,
                'created_at': message.created_at.astimezone(
                    __import__('zoneinfo').ZoneInfo('Asia/Kathmandu')
                ).strftime('%I:%M %p'),
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'sender_id': event['sender_id'],
            'created_at': event['created_at'],
        }))

    @database_sync_to_async
    def user_can_access_booking(self, user, booking_id):
        try:
            booking = Booking.objects.get(pk=booking_id)
        except Booking.DoesNotExist:
            return False
        return booking.customer_id == user.id or booking.provider.user_id == user.id

    @database_sync_to_async
    def save_message(self, user, booking_id, content):
        return Message.objects.create(booking_id=booking_id, sender=user, content=content)
