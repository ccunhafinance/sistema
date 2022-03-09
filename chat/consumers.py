import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser

user = CustomUser

class ChatConsumers(AsyncConsumer):
    async def websocket_connect(self, event):
        print('conected', event)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receiver(self, event):
        print('receive', event)

    async def websocket_disconnect(self, event):
        print('disconeccted', event)