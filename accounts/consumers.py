from channels.generic.websocket import AsyncWebsocketConsumer
import json

class EmailStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.email_id = self.scope['url_route']['kwargs']['email_id']
        self.group_name = f"email_{self.email_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def email_status(self, event):
        await self.send(text_data=json.dumps({
            'status': event['status']
        }))
