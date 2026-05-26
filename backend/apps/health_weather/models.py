"""
Health Weather models — AQI, UV index, pollen, and wellness indexes.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class HealthMetric(TimeStampedModel):
    """Health related metrics based on weather conditions."""
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    aqi = models.IntegerField(help_text='Air Quality Index')
    uv_index = models.FloatField()
    pollen_tree = models.CharField(max_length=20, default='Low')
    pollen_grass = models.CharField(max_length=20, default='Low')
    pollen_ragweed = models.CharField(max_length=20, default='Low')
    joint_pain_index = models.IntegerField(help_text='Joint pain risk scale 1-10', default=2)
    asthma_risk = models.CharField(max_length=20, default='Low')
    flu_risk = models.CharField(max_length=20, default='Low')

    class Meta:
        db_table = 'health_metrics'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.location_name} (AQI: {self.aqi}, UV: {self.uv_index})"
