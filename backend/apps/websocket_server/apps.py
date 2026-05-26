from django.apps import AppConfig


class WebsocketServerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.websocket_server'
    verbose_name = 'WebSocket Server'
