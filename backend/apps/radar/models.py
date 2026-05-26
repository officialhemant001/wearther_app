"""
Radar models — radar frames.
"""

from django.db import models
from apps.core.models import TimeStampedModel


class RadarFrame(TimeStampedModel):
    """Radar image frame at a timestamp."""
    timestamp = models.DateTimeField(db_index=True)
    image_url = models.CharField(max_length=500)
    layer = models.CharField(max_length=50, default='precipitation')

    class Meta:
        db_table = 'radar_frames'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.layer} - {self.timestamp}"
