"""
Alerts models — custom user alert rules and triggered alerts.
"""

from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class AlertRule(UUIDModel):
    """User-defined rules for custom weather alerts."""
    CONDITION_CHOICES = [
        ('above', 'Above'),
        ('below', 'Below'),
        ('equals', 'Equals'),
    ]
    METRIC_CHOICES = [
        ('temperature', 'Temperature (°C)'),
        ('humidity', 'Humidity (%)'),
        ('wind_speed', 'Wind Speed (m/s)'),
        ('aqi', 'Air Quality Index'),
        ('uv_index', 'UV Index'),
        ('rain', 'Rain probability'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alert_rules')
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location_name = models.CharField(max_length=255)
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    threshold = models.FloatField()
    is_active = models.BooleanField(default=True)
    last_triggered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'alert_rules'

    def __str__(self):
        return f"{self.user.email} - {self.name} ({self.metric} {self.condition} {self.threshold})"


class WeatherAlert(UUIDModel):
    """Triggered weather alerts based on rules or official sources."""
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('danger', 'Danger'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='weather_alerts')
    rule = models.ForeignKey(AlertRule, on_delete=models.SET_NULL, null=True, blank=True, related_name='triggered_alerts')
    title = models.CharField(max_length=255)
    message = models.TextField()
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    source = models.CharField(max_length=100, default='system')

    class Meta:
        db_table = 'weather_alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.severity})"
