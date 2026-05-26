"""
Channels consumers for real-time weather alerts and updates.
"""

import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class WeatherConsumer(AsyncJsonWebsocketConsumer):
    """Consumer for serving real-time updates for a location."""
    async def connect(self):
        self.location_name = self.scope['url_route']['kwargs']['location_name']
        self.room_group_name = f"weather_{self.location_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content):
        """Receive message from Client WebSocket."""
        # Custom client requests can trigger immediate queries
        await self.send_json({
            'success': True,
            'message': f"Echoing request for weather: {content.get('query')}"
        })

    async def weather_update(self, event):
        """Receive weather update notification from group."""
        await self.send_json({
            'type': 'weather_update',
            'data': event['data']
        })
