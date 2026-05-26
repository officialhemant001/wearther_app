"""
Locations models — saved cities and search history.
"""

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class SavedLocation(TimeStampedModel):
    """Locations saved by users for quick weather access."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_locations')
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    country = models.CharField(max_length=10, blank=True)
    state = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    custom_name = models.CharField(max_length=255, blank=True, help_text='User customized label')

    class Meta:
        db_table = 'saved_locations'
        unique_together = ('user', 'latitude', 'longitude')

    def __str__(self):
        return f"{self.user.email} - {self.custom_name or self.name}"
