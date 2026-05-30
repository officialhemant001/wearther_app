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
            return self._fetch_open_meteo_weather(lat, lon)

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
            return self._fetch_open_meteo_weather(lat, lon)

    def get_forecast(self, lat, lon, days=7):
        """Fetch forecast data."""
        if self.API_KEY == 'demo':
            return self._fetch_open_meteo_forecast(lat, lon, days)

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
            return self._fetch_open_meteo_forecast(lat, lon, days)

    def get_air_quality(self, lat, lon):
        """Fetch air quality data."""
        if self.API_KEY == 'demo':
            return self._fetch_open_meteo_aqi(lat, lon)

        try:
            url = f"http://api.openweathermap.org/data/2.5/air_pollution"
            params = {'lat': lat, 'lon': lon, 'appid': self.API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"AQI API error: {e}")
            return self._fetch_open_meteo_aqi(lat, lon)

    def search_location(self, query):
        """Geocode a location name."""
        if not query:
            return []
        if self.API_KEY == 'demo':
            return self._fetch_open_meteo_geocoding(query)

        try:
            url = "http://api.openweathermap.org/geo/1.0/direct"
            params = {'q': query, 'limit': 5, 'appid': self.API_KEY}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Geocoding error: {e}")
            return self._fetch_open_meteo_geocoding(query)

    def _fetch_open_meteo_weather(self, lat, lon):
        """Fetch real-time weather from Open-Meteo's key-less API."""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,cloud_cover,pressure_msl,wind_speed_10m,wind_direction_10m,wind_gusts_10m',
                'timezone': 'auto'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current', {})
            wmo_code = current.get('weather_code', 0)
            main, desc, icon = self._map_wmo_to_owm(wmo_code)
            
            return {
                'location_name': 'Hyperspatial Coordinates',
                'latitude': lat,
                'longitude': lon,
                'temperature': current.get('temperature_2m', 32.5),
                'feels_like': current.get('apparent_temperature', 35.2),
                'temp_min': current.get('temperature_2m', 28.0),
                'temp_max': current.get('temperature_2m', 36.0),
                'humidity': current.get('relative_humidity_2m', 65),
                'pressure': current.get('pressure_msl', 1013.25),
                'wind_speed': current.get('wind_speed_10m', 3.5),
                'wind_direction': current.get('wind_direction_10m', 180),
                'wind_gust': current.get('wind_gusts_10m', 5.2),
                'visibility': 10000,
                'clouds': current.get('cloud_cover', 40),
                'weather_main': main,
                'weather_description': desc,
                'weather_icon': icon,
                'sunrise': None,
                'sunset': None,
                'rain_1h': current.get('rain'),
                'snow_1h': current.get('snowfall'),
                'uv_index': 5.0,
                'dew_point': 12.0,
            }
        except Exception as e:
            logger.error(f"Open-Meteo weather fetch error: {e}")
            return self._get_demo_weather(lat, lon)

    def _fetch_open_meteo_forecast(self, lat, lon, days=7):
        """Fetch forecasts from Open-Meteo and return frontend-friendly and OWM-compatible formats."""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': lat,
                'longitude': lon,
                'daily': 'temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max,relative_humidity_2m_max,weather_code',
                'hourly': 'temperature_2m,relative_humidity_2m,weather_code',
                'timezone': 'auto',
                'forecast_days': days
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            daily_data = data.get('daily', {})
            hourly_data = data.get('hourly', {})
            
            forecasts_list = []
            daily_forecasts = []
            hourly_forecasts = []
            
            days_count = len(daily_data.get('time', []))
            for i in range(days_count):
                date_str = daily_data['time'][i]
                dt = datetime.strptime(date_str, '%Y-%m-%d')
                day_name = dt.strftime('%A')
                if i == 0:
                    day_name = 'Today'
                elif i == 1:
                    day_name = 'Tomorrow'
                    
                wmo_code = daily_data['weather_code'][i]
                main, desc, icon = self._map_wmo_to_owm(wmo_code)
                
                temp_min = daily_data['temperature_2m_min'][i]
                temp_max = daily_data['temperature_2m_max'][i]
                humidity = daily_data.get('relative_humidity_2m_max', [60]*days_count)[i]
                wind_speed = daily_data['wind_speed_10m_max'][i]
                rain_prob = daily_data['precipitation_probability_max'][i]
                
                daily_forecasts.append({
                    'day': day_name,
                    'condition': main,
                    'high': round(temp_max),
                    'low': round(temp_min),
                    'rain': round(rain_prob),
                    'wind': round(wind_speed, 1),
                    'humidity': round(humidity),
                })
                
                hourly_list = []
                date_prefix = date_str
                for h_idx, h_time in enumerate(hourly_data.get('time', [])):
                    if h_time.startswith(date_prefix):
                        time_part = h_time.split('T')[1][:5]
                        h_wmo = hourly_data['weather_code'][h_idx]
                        h_main, h_desc, h_icon = self._map_wmo_to_owm(h_wmo)
                        hourly_list.append({
                            'time': time_part,
                            'temperature': round(hourly_data['temperature_2m'][h_idx], 1),
                            'humidity': round(hourly_data['relative_humidity_2m'][h_idx]),
                            'weather_icon': h_icon,
                        })
                
                forecasts_list.append({
                    'date': date_str,
                    'temp_min': round(temp_min, 1),
                    'temp_max': round(temp_max, 1),
                    'humidity': round(humidity),
                    'wind_speed': round(wind_speed, 1),
                    'weather_main': main,
                    'weather_description': desc,
                    'weather_icon': icon,
                    'pop': round(rain_prob / 100.0, 2),
                    'hourly': hourly_list,
                })
            
            for j in range(0, 24, 2):
                if j < len(hourly_data.get('time', [])):
                    time_str = hourly_data['time'][j]
                    time_part = time_str.split('T')[1][:5]
                    h_wmo = hourly_data['weather_code'][j]
                    h_main, h_desc, h_icon = self._map_wmo_to_owm(h_wmo)
                    hourly_forecasts.append({
                        'time': time_part,
                        'temp': round(hourly_data['temperature_2m'][j]),
                        'condition': h_main,
                    })
                    
            return {
                'forecasts': forecasts_list,
                'daily': daily_forecasts,
                'hourly': hourly_forecasts,
            }
        except Exception as e:
            logger.error(f"Open-Meteo forecast error: {e}")
            return self._get_demo_forecast(lat, lon, days)

    def _fetch_open_meteo_aqi(self, lat, lon):
        """Fetch real-time air quality metrics from Open-Meteo Air Quality API."""
        try:
            url = "https://air-quality-api.open-meteo.com/v1/air-quality"
            params = {
                'latitude': lat,
                'longitude': lon,
                'current': 'european_aqi,pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,sulphur_dioxide,ozone',
                'timezone': 'auto'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            current = data.get('current', {})
            aqi_val = current.get('european_aqi', 1)
            
            aqi_labels = {
                1: 'Good',
                2: 'Fair',
                3: 'Moderate',
                4: 'Poor',
                5: 'Very Poor'
            }
            aqi_label = aqi_labels.get(aqi_val, 'Moderate')
            if aqi_val > 5:
                aqi_val = 5
                aqi_label = 'Very Poor'
                
            return {
                'aqi': aqi_val,
                'aqi_label': aqi_label,
                'co': current.get('carbon_monoxide', 250.34),
                'no': 0.1,
                'no2': current.get('nitrogen_dioxide', 12.5),
                'o3': current.get('ozone', 68.2),
                'so2': current.get('sulphur_dioxide', 5.2),
                'pm2_5': current.get('pm2_5', 35.4),
                'pm10': current.get('pm10', 52.1),
                'nh3': 1.0,
            }
        except Exception as e:
            logger.error(f"Open-Meteo AQI error: {e}")
            return self._get_demo_aqi(lat, lon)

    def _fetch_open_meteo_geocoding(self, query):
        """Search location dynamically using Open-Meteo Geocoding Search API."""
        try:
            url = "https://geocoding-api.open-meteo.com/v1/search"
            params = {'name': query, 'count': 5, 'language': 'en', 'format': 'json'}
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = data.get('results', [])
            mapped = []
            for r in results:
                mapped.append({
                    'name': r.get('name'),
                    'lat': r.get('latitude'),
                    'lon': r.get('longitude'),
                    'country': r.get('country_code'),
                    'state': r.get('admin1'),
                })
            return mapped if mapped else self._get_demo_locations(query)
        except Exception as e:
            logger.error(f"Open-Meteo geocoding error: {e}")
            return self._get_demo_locations(query)

    def _map_wmo_to_owm(self, code):
        """Map WMO Weather interpretation codes (0-99) to OpenWeatherMap main, description and icon."""
        mapping = {
            0: ('Clear', 'clear sky', '01d'),
            1: ('Clouds', 'mainly clear', '02d'),
            2: ('Clouds', 'partly cloudy', '03d'),
            3: ('Clouds', 'overcast', '04d'),
            45: ('Clouds', 'foggy', '50d'),
            48: ('Clouds', 'depositing rime fog', '50d'),
            51: ('Drizzle', 'light drizzle', '09d'),
            53: ('Drizzle', 'moderate drizzle', '09d'),
            55: ('Drizzle', 'dense drizzle', '09d'),
            56: ('Drizzle', 'light freezing drizzle', '09d'),
            57: ('Drizzle', 'dense freezing drizzle', '09d'),
            61: ('Rain', 'slight rain', '10d'),
            63: ('Rain', 'moderate rain', '10d'),
            65: ('Rain', 'heavy rain', '10d'),
            66: ('Rain', 'light freezing rain', '10d'),
            67: ('Rain', 'heavy freezing rain', '10d'),
            71: ('Snow', 'slight snow fall', '13d'),
            73: ('Snow', 'moderate snow fall', '13d'),
            75: ('Snow', 'heavy snow fall', '13d'),
            77: ('Snow', 'snow grains', '13d'),
            80: ('Rain', 'slight rain showers', '09d'),
            81: ('Rain', 'moderate rain showers', '09d'),
            82: ('Rain', 'violent rain showers', '09d'),
            85: ('Snow', 'slight snow showers', '13d'),
            86: ('Snow', 'heavy snow showers', '13d'),
            95: ('Thunderstorm', 'thunderstorm', '11d'),
            96: ('Thunderstorm', 'thunderstorm with slight hail', '11d'),
            99: ('Thunderstorm', 'thunderstorm with heavy hail', '11d'),
        }
        return mapping.get(code, ('Clouds', 'overcast', '03d'))

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
