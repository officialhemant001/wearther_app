from rest_framework import serializers
from .models import WeatherData


class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = '__all__'


class CurrentWeatherSerializer(serializers.Serializer):
    """Serializer for current weather response."""
    location_name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    temperature = serializers.FloatField()
    feels_like = serializers.FloatField(allow_null=True)
    temp_min = serializers.FloatField(allow_null=True)
    temp_max = serializers.FloatField(allow_null=True)
    humidity = serializers.IntegerField(allow_null=True)
    pressure = serializers.FloatField(allow_null=True)
    wind_speed = serializers.FloatField(allow_null=True)
    wind_direction = serializers.IntegerField(allow_null=True)
    wind_gust = serializers.FloatField(allow_null=True)
    visibility = serializers.IntegerField(allow_null=True)
    clouds = serializers.IntegerField(allow_null=True)
    weather_main = serializers.CharField()
    weather_description = serializers.CharField()
    weather_icon = serializers.CharField()
    sunrise = serializers.CharField(allow_null=True)
    sunset = serializers.CharField(allow_null=True)
    uv_index = serializers.FloatField(allow_null=True)
    dew_point = serializers.FloatField(allow_null=True)


class WeatherQuerySerializer(serializers.Serializer):
    """Query params for weather requests."""
    lat = serializers.FloatField(required=False, default=28.6139)
    lon = serializers.FloatField(required=False, default=77.2090)
    city = serializers.CharField(required=False)
