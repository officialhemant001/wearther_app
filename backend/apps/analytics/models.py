"""
Analytics models — user activity logs and query tracking.
"""

from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class UserActivityLog(TimeStampedModel):
    """Logs user actions for analytics."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='activities', null=True, blank=True)
    action = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        db_table = 'user_activity_logs'

    def __str__(self):
        return f"{self.user.email if self.user else 'Anon'} - {self.action}"
