"""
Weather app — current weather data models and services.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class WeatherData(TimeStampedModel):
    """Stored weather data for a location."""
    location_name = models.CharField(max_length=255, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    temperature = models.FloatField(help_text='Temperature in Celsius')
    feels_like = models.FloatField(null=True)
    temp_min = models.FloatField(null=True)
    temp_max = models.FloatField(null=True)
    humidity = models.IntegerField(null=True)
    pressure = models.FloatField(null=True, help_text='Pressure in hPa')
    wind_speed = models.FloatField(null=True, help_text='Wind speed in m/s')
    wind_direction = models.IntegerField(null=True, help_text='Wind direction in degrees')
    wind_gust = models.FloatField(null=True)
    visibility = models.IntegerField(null=True, help_text='Visibility in meters')
    clouds = models.IntegerField(null=True, help_text='Cloudiness percentage')
    weather_main = models.CharField(max_length=50, blank=True)
    weather_description = models.CharField(max_length=255, blank=True)
    weather_icon = models.CharField(max_length=10, blank=True)
    sunrise = models.DateTimeField(null=True)
    sunset = models.DateTimeField(null=True)
    rain_1h = models.FloatField(null=True, help_text='Rain volume for last 1h in mm')
    snow_1h = models.FloatField(null=True, help_text='Snow volume for last 1h in mm')
    uv_index = models.FloatField(null=True)
    dew_point = models.FloatField(null=True)
    source = models.CharField(max_length=50, default='openweathermap')
    raw_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'weather_data'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['location_name', '-created_at']),
        ]

    def __str__(self):
        return f"{self.location_name}: {self.temperature}°C ({self.weather_main})"
