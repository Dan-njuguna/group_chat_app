from django.urls import path

from . import consumers

websocket_urlpatterns = [
  path('ws//', consumers.ChatConsumer.as_asgi()), # Using asgi
]
# Receive message from WebSocket
async def receive(self, text_data):
  data = json.loads(text_data)
  message = data['message']
  username = data['username']
  room = data['room']

  # Send message to room group
  await self.channel_layer.group_send(
    self.room_group_name,
    {
      'type': 'chat_message',
      'message': message,
      'username': username
    }
  )

# Receive message from room group
async def chat_message(self, event):
  message = event['message']
  username = event['username']

  # Send message to WebSocket
  await self.send(text_data=json.dumps({
    'message': message,
    'username': username
  }))
  