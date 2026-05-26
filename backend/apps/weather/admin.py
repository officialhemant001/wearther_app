from django.contrib import admin
from .models import WeatherData


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location_name', 'temperature', 'weather_main', 'humidity', 'created_at']
    list_filter = ['weather_main', 'source']
    search_fields = ['location_name']
