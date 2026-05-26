"""
Subscriptions models — plans and payment tracking.
"""

from django.db import models
from django.conf import settings
from apps.core.models import UUIDModel


class Plan(UUIDModel):
    """Premium tier plans."""
    name = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.JSONField(help_text='JSON list of features')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscription_plans'

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Subscription(UUIDModel):
    """User plan subscription record."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('expired', 'Expired'),
        ('trialing', 'Trialing'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)

    class Meta:
        db_table = 'user_subscriptions'

    def __str__(self):
        return f"{self.user.email} - {self.plan.name} ({self.status})"
