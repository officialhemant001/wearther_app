from rest_framework import serializers
from .models import WeatherRecommendation


class WeatherRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherRecommendation
        fields = '__all__'
