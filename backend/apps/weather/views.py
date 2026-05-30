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
    """Get hyperlocal weather with precise coordinates or resolved city name."""
    permission_classes = [AllowAny]

    def get(self, request):
        city = request.query_params.get('city')
        service = WeatherService()
        location_name = None

        if city:
            locations = service.search_location(city)
            if locations:
                loc = locations[0]
                lat = float(loc.get('lat', 28.6139))
                lon = float(loc.get('lon', 77.2090))
                name = loc.get('name', city)
                country = loc.get('country')
                state = loc.get('state')
                if name:
                    if state and country:
                        location_name = f"{name}, {state}, {country}"
                    elif country:
                        location_name = f"{name}, {country}"
                    else:
                        location_name = name
            else:
                lat = float(request.query_params.get('lat', 28.6139))
                lon = float(request.query_params.get('lon', 77.2090))
        else:
            lat = float(request.query_params.get('lat', 28.6139))
            lon = float(request.query_params.get('lon', 77.2090))

        weather = service.get_current_weather(lat, lon)
        
        if location_name and isinstance(weather, dict):
            weather['location_name'] = location_name
        elif city and isinstance(weather, dict) and not weather.get('location_name'):
            weather['location_name'] = city

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
