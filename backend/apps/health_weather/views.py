from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response
from .models import HealthMetric
from .serializers import HealthMetricSerializer


class HealthWeatherView(APIView):
    """Retrieve health-specific weather metrics and suggestions."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))

        # Returns details regarding joint pain, asthma, and allergy risk indices
        data = {
            'latitude': lat,
            'longitude': lon,
            'aqi': 85,
            'aqi_status': 'Moderate',
            'uv_index': 6.2,
            'uv_status': 'High',
            'pollen': {
                'tree': 'Moderate',
                'grass': 'Low',
                'ragweed': 'Low',
            },
            'wellness_risks': {
                'asthma': 'Moderate risk due to particulate matter',
                'joint_pain': 'Low risk (warm and dry)',
                'migraine': 'Low risk',
                'influenza': 'Very low risk',
            },
            'recommendations': [
                'Wear sunscreen (SPF 30+) if outdoors.',
                'Sensitive individuals should limit prolonged outdoor exertion.',
                'Keep inhalers close if asthma-prone due to moderate air quality.'
            ]
        }

        return Response(success_response(data=data, message='Health weather indices'))
