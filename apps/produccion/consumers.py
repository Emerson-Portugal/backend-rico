#apps/produccion/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificacionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.usuario = self.scope['user']
        if self.usuario.is_authenticated:
            self.group_name = f"notificaciones_{self.usuario.username}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()
    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def recibir_notificacion(self, event):
        await self.send(text_data=json.dumps({
            "mensaje": event["mensaje"]
        }))


