"""
WebSocket URL routing.
"""

from django.urls import re_path
from .consumers import WeatherConsumer

websocket_urlpatterns = [
    re_path(r'ws/weather/(?P<location_name>\w+)/$', WeatherConsumer.as_asgi()),
]
