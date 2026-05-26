from rest_framework import serializers
from .models import DailyForecast, HourlyForecast


class HourlyForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = HourlyForecast
        exclude = ['daily_forecast']


class DailyForecastSerializer(serializers.ModelSerializer):
    hourly_forecasts = HourlyForecastSerializer(many=True, read_only=True)

    class Meta:
        model = DailyForecast
        fields = '__all__'
