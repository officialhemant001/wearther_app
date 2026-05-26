from rest_framework import serializers
from .models import AlertRule, WeatherAlert


class AlertRuleSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = AlertRule
        fields = '__all__'
        read_only_fields = ['last_triggered_at']


class WeatherAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherAlert
        fields = '__all__'
