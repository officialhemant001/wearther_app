from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.core.utils import success_response
from django.utils import timezone
from .models import UserActivityLog
from .serializers import UserActivityLogSerializer


class AnalyticsSummaryView(APIView):
    """Admin-only view for dashboard telemetry."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        # Generates basic metrics on total operations
        from apps.users.models import User
        from apps.weather.models import WeatherData

        data = {
            'total_users': User.objects.count(),
            'active_users_today': User.objects.filter(last_login__date=timezone.now().date()).count(),
            'weather_queries_served': WeatherData.objects.count(),
            'recent_logs': UserActivityLogSerializer(UserActivityLog.objects.all()[:10], many=True).data
        }
        return Response(success_response(data=data, message='Analytics Summary'))
