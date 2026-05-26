"""
Forecasts models for hourly, daily, and weekly forecasts.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class DailyForecast(TimeStampedModel):
    """Daily weather forecast."""
    location_name = models.CharField(max_length=255, db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    date = models.DateField(db_index=True)
    temp_min = models.FloatField(help_text='Min temperature in Celsius')
    temp_max = models.FloatField(help_text='Max temperature in Celsius')
    temp_morn = models.FloatField(null=True)
    temp_day = models.FloatField(null=True)
    temp_eve = models.FloatField(null=True)
    temp_night = models.FloatField(null=True)
    humidity = models.IntegerField(null=True)
    pressure = models.FloatField(null=True)
    wind_speed = models.FloatField(null=True)
    wind_direction = models.IntegerField(null=True)
    weather_main = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=255)
    weather_icon = models.CharField(max_length=10)
    pop = models.FloatField(default=0.0, help_text='Probability of precipitation (0.0 to 1.0)')
    rain = models.FloatField(default=0.0, help_text='Rain volume in mm')
    snow = models.FloatField(default=0.0, help_text='Snow volume in mm')
    uv_index = models.FloatField(null=True)

    class Meta:
        db_table = 'daily_forecasts'
        ordering = ['date']
        unique_together = ('latitude', 'longitude', 'date')

    def __str__(self):
        return f"{self.location_name} - {self.date}: {self.temp_min}°C to {self.temp_max}°C"


class HourlyForecast(TimeStampedModel):
    """Hourly weather forecast."""
    daily_forecast = models.ForeignKey(DailyForecast, on_delete=models.CASCADE, related_name='hourly_forecasts', null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    time = models.DateTimeField(db_index=True)
    temperature = models.FloatField()
    feels_like = models.FloatField(null=True)
    humidity = models.IntegerField(null=True)
    pressure = models.FloatField(null=True)
    wind_speed = models.FloatField(null=True)
    wind_direction = models.IntegerField(null=True)
    weather_main = models.CharField(max_length=50)
    weather_description = models.CharField(max_length=255)
    weather_icon = models.CharField(max_length=10)
    pop = models.FloatField(default=0.0, help_text='Probability of precipitation')
    rain = models.FloatField(default=0.0)
    snow = models.FloatField(default=0.0)

    class Meta:
        db_table = 'hourly_forecasts'
        ordering = ['time']
        unique_together = ('latitude', 'longitude', 'time')

    def __str__(self):
        return f"{self.time}: {self.temperature}°C"
