"""
Weather data services — OpenWeatherMap API integration.
"""

import requests
import logging
from django.conf import settings
from datetime import datetime, timezone as tz

logger = logging.getLogger(__name__)


class WeatherService:
    """Service for fetching weather data from OpenWeatherMap API."""

    BASE_URL = None
    API_KEY = None

    def __init__(self):
        self.BASE_URL = settings.WEATHER_API_BASE_URL
        self.API_KEY = settings.OPENWEATHERMAP_API_KEY

    def get_current_weather(self, lat, lon):
        """Fetch current weather for coordinates."""
        if self.API_KEY == 'demo':
            return self._get_demo_weather(lat, lon)

        try:
            url = f"{self.BASE_URL}/weather"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.API_KEY,
                'units': 'metric',
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            return self._parse_current_weather(data)
        except Exception as e:
            logger.error(f"Weather API error: {e}")
            return self._get_demo_weather(lat, lon)

    def get_forecast(self, lat, lon, days=7):
        """Fetch forecast data."""
        if self.API_KEY == 'demo':
            return self._get_demo_forecast(lat, lon, days)

        try:
            url = f"{self.BASE_URL}/forecast"
            params = {
                'lat': lat,
                'lon': lon,
                'appid': self.API_KEY,
                'units': 'metric',
                'cnt': days * 8,  # 3-hour intervals
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Forecast API error: {e}")
            return self._get_demo_forecast(lat, lon, days)

    def get_air_quality(self, lat, lon):
        """Fetch air quality data."""
        if self.API_KEY == 'demo':
            return self._get_demo_aqi(lat, lon)

        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution"
            params = {'lat': lat, 'lon': lon, 'appid': self.API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"AQI API error: {e}")
            return self._get_demo_aqi(lat, lon)

    def search_location(self, query):
        """Geocode a location name."""
        if self.API_KEY == 'demo':
            return self._get_demo_locations(query)

        try:
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {'q': query, 'limit': 5, 'appid': self.API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return self._get_demo_locations(query)

    # ==================================================
    # Demo data (when no API key is configured)
    # ==================================================

    def _get_demo_weather(self, lat, lon):
        """Return realistic demo weather data."""
        return {
            'location_name': 'New Delhi',
            'latitude': lat,
            'longitude': lon,
            'temperature': 32.5,
            'feels_like': 35.2,
            'temp_min': 28.0,
            'temp_max': 36.0,
            'humidity': 65,
            'pressure': 1013.25,
            'wind_speed': 3.5,
            'wind_direction': 180,
            'wind_gust': 5.2,
            'visibility': 10000,
            'clouds': 40,
            'weather_main': 'Clouds',
            'weather_description': 'scattered clouds',
            'weather_icon': '03d',
            'sunrise': '2026-05-26T05:30:00+05:30',
            'sunset': '2026-05-26T19:15:00+05:30',
            'rain_1h': None,
            'snow_1h': None,
            'uv_index': 8.5,
            'dew_point': 22.3,
        }

    def _get_demo_forecast(self, lat, lon, days):
        """Return demo forecast data."""
        import random
        forecasts = []
        for i in range(days):
            forecasts.append({
                'date': f'2026-05-{27 + i:02d}',
                'temp_min': round(random.uniform(24, 28), 1),
                'temp_max': round(random.uniform(32, 38), 1),
                'humidity': random.randint(40, 80),
                'wind_speed': round(random.uniform(1, 8), 1),
                'weather_main': random.choice(['Clear', 'Clouds', 'Rain', 'Thunderstorm']),
                'weather_description': 'partly cloudy',
                'weather_icon': random.choice(['01d', '02d', '03d', '10d']),
                'pop': round(random.uniform(0, 0.8), 2),
                'hourly': [
                    {
                        'time': f'{h:02d}:00',
                        'temperature': round(random.uniform(24, 38), 1),
                        'humidity': random.randint(30, 90),
                        'weather_icon': '01d' if 6 <= h <= 18 else '01n',
                    }
                    for h in range(0, 24, 3)
                ],
            })
        return {'forecasts': forecasts}

    def _get_demo_aqi(self, lat, lon):
        """Return demo AQI data."""
        return {
            'aqi': 3,
            'aqi_label': 'Moderate',
            'co': 250.34,
            'no': 0.23,
            'no2': 12.5,
            'o3': 68.2,
            'so2': 5.2,
            'pm2_5': 35.4,
            'pm10': 52.1,
            'nh3': 2.3,
        }

    def _get_demo_locations(self, query):
        """Return demo location results."""
        return [
            {'name': 'New Delhi', 'lat': 28.6139, 'lon': 77.2090, 'country': 'IN', 'state': 'Delhi'},
            {'name': 'Mumbai', 'lat': 19.0760, 'lon': 72.8777, 'country': 'IN', 'state': 'Maharashtra'},
            {'name': 'London', 'lat': 51.5074, 'lon': -0.1278, 'country': 'GB', 'state': 'England'},
        ]

    def _parse_current_weather(self, data):
        """Parse OpenWeatherMap API response."""
        weather = data.get('weather', [{}])[0]
        main = data.get('main', {})
        wind = data.get('wind', {})
        sys = data.get('sys', {})

        return {
            'location_name': data.get('name', ''),
            'latitude': data.get('coord', {}).get('lat'),
            'longitude': data.get('coord', {}).get('lon'),
            'temperature': main.get('temp'),
            'feels_like': main.get('feels_like'),
            'temp_min': main.get('temp_min'),
            'temp_max': main.get('temp_max'),
            'humidity': main.get('humidity'),
            'pressure': main.get('pressure'),
            'wind_speed': wind.get('speed'),
            'wind_direction': wind.get('deg'),
            'wind_gust': wind.get('gust'),
            'visibility': data.get('visibility'),
            'clouds': data.get('clouds', {}).get('all'),
            'weather_main': weather.get('main', ''),
            'weather_description': weather.get('description', ''),
            'weather_icon': weather.get('icon', ''),
            'sunrise': datetime.fromtimestamp(sys.get('sunrise', 0), tz=tz.utc).isoformat() if sys.get('sunrise') else None,
            'sunset': datetime.fromtimestamp(sys.get('sunset', 0), tz=tz.utc).isoformat() if sys.get('sunset') else None,
            'rain_1h': data.get('rain', {}).get('1h'),
            'snow_1h': data.get('snow', {}).get('1h'),
            'uv_index': None,
            'dew_point': None,
        }
