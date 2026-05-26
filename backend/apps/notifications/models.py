"""
Notifications models — in-app notifications and preferences.
"""

from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class Notification(UUIDModel):
    """System and user notifications."""
    TYPE_CHOICES = [
        ('system', 'System Update'),
        ('alert', 'Weather Alert'),
        ('billing', 'Billing & Subscription'),
        ('recommendation', 'Personal Recommendation'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=255, blank=True)
    meta_data = models.JSONField(null=True, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title} ({self.notification_type})"
