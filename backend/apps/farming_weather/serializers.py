from rest_framework import serializers
from .models import FarmingMetrics


class FarmingMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmingMetrics
        fields = '__all__'
