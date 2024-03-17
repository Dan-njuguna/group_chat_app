import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.roomName = "Group"
        await self.channel_layer.group_add(
            self.roomName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.roomGroupName,
            self.channel_layer
        )
    
    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
            username = text_data_json['username']
            await self.channel_layer.group_send(
                self.roomGroupName, {
                    "type": "sendMessage",
                    "message": message,
                    "username": username,
                }
            )
        except Exception as e:
            print(f"Error: '{e}'")

        send_message_to_channel(message, username)


    async def sendMessage(self, event):
       message = event["message"]
       username = event["username"]
       await self.send(text_data = json.dumps({"message": message, "username": username}))



from channels.layers import get_channel_layer


def send_message_to_channel(message, username):
    channel_layer = get_channel_layer()

    async def send_message_task():
        await channel_layer.group_send(
            "group_chat",
            {
                "type": "sendMessage",
                "message": message,
                "username": username,
            }
        )

    asyncio.run(send_message_task())
