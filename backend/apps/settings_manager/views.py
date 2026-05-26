from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response


class AppSettingsView(APIView):
    """Retrieve app-wide settings and configuration flags."""
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            'app_version': '1.0.0',
            'support_email': 'support@weatherapp.next',
            'maintenance_mode': False,
            'features': {
                'ai_chat': True,
                'farming_weather': True,
                'health_advisory': True,
                'radar_animation': True,
            }
        }
        return Response(success_response(data=data, message='App configurations'))
