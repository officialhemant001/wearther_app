from rest_framework import serializers
from .models import RadarFrame


class RadarFrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RadarFrame
        fields = '__all__'
