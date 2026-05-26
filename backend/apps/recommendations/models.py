"""
Recommendations models — personalized activity suggestions.
"""

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class WeatherRecommendation(TimeStampedModel):
    """Personalized suggestions linked to current weather parameters."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recommendations')
    activity_name = models.CharField(max_length=100)
    suitability = models.CharField(max_length=20, default='Good')
    reason = models.TextField()

    class Meta:
        db_table = 'weather_recommendations'

    def __str__(self):
        return f"{self.user.email} - {self.activity_name}: {self.suitability}"
