from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response
from .services import WeatherService


class CurrentWeatherView(APIView):
    """Get current weather for a location."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))

        service = WeatherService()
        data = service.get_current_weather(lat, lon)

        return Response(success_response(data=data, message='Current weather data'))


class HyperlocalWeatherView(APIView):
    """Get hyperlocal weather with precise coordinates."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))

        service = WeatherService()
        weather = service.get_current_weather(lat, lon)
        aqi = service.get_air_quality(lat, lon)

        data = {
            'weather': weather,
            'air_quality': aqi,
            'is_hyperlocal': True,
        }

        return Response(success_response(data=data, message='Hyperlocal weather data'))


class WeatherSearchView(APIView):
    """Search for weather by city name."""
    permission_classes = [AllowAny]

    def get(self, request):
        query = request.query_params.get('q', '')
        service = WeatherService()
        locations = service.search_location(query)
        return Response(success_response(data=locations, message='Location search results'))
