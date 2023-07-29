import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message







class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        user = self.scope['user']

        self.room_group_name = f'chat_{user.id}'

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_text = data['message']

        user = self.scope['user']
        chat_id = data['chat_id']

        try:
            chat = Chat.objects.get(id=chat_id)
        except Chat.DoesNotExist:
            return

        message = Message.objects.create(chat=chat, sender=user, text=message_text)

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message.text,
                'user': user.username,
            }
        )

    async def chat_message(self, event):
        # Send the message to the WebSocket
        message = event['message']
        user = event['user']

        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))