from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response
from apps.weather.services import WeatherService
from .serializers import DailyForecastSerializer, HourlyForecastSerializer


class ForecastView(APIView):
    """Retrieve weather forecast for a location."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))
        days = int(request.query_params.get('days', 7))

        service = WeatherService()
        data = service.get_forecast(lat, lon, days)

        return Response(success_response(data=data, message=f"{days}-day weather forecast"))
