"""
Farming Weather models — agricultural conditions.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class FarmingMetrics(TimeStampedModel):
    """Agricultural weather parameters."""
    location_name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    soil_temperature = models.FloatField(help_text='Soil temperature in Celsius at 10cm depth')
    soil_moisture = models.FloatField(help_text='Soil moisture percentage')
    evapotranspiration = models.FloatField(help_text='Daily rate in mm')
    leaf_wetness = models.FloatField(help_text='Leaf wetness duration in hours')

    class Meta:
        db_table = 'farming_metrics'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.location_name} (Soil Temp: {self.soil_temperature}°C, Moisture: {self.soil_moisture}%)"
