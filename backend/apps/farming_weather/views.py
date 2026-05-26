from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response
from .models import FarmingMetrics
from .serializers import FarmingMetricsSerializer


class FarmingWeatherView(APIView):
    """Retrieve agricultural weather insights."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))

        # Returns details regarding soil properties and crop advisory suggestions
        data = {
            'latitude': lat,
            'longitude': lon,
            'soil': {
                'temperature': 24.2,
                'moisture_percentage': 58,
                'status': 'Optimal moisture for planting',
            },
            'evapotranspiration_rate': '3.2 mm/day',
            'crop_advisories': [
                {
                    'crop': 'Wheat',
                    'stage': 'Tillering stage',
                    'advisory': 'Maintain irrigation schedule. Light showers forecast in 48h may reduce irrigation needs.'
                },
                {
                    'crop': 'Rice',
                    'stage': 'Nursery stage',
                    'advisory': 'Keep fields flooded to 2-3 cm. Watch for leaf wetness indicators indicating blast risk.'
                }
            ],
            'spraying_conditions': {
                'status': 'Good',
                'reason': 'Wind speeds are below 8 km/h and relative humidity is optimal.'
            }
        }

        return Response(success_response(data=data, message='Farming weather insights'))
