"""
Custom User model and related models for the Weather Application.
"""

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .managers import CustomUserManager


class User(AbstractUser):
    """Custom user model with email as the primary identifier."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(
        max_length=20,
        choices=[
            ('email', 'Email'),
            ('google', 'Google'),
            ('phone', 'Phone'),
        ],
        default='email',
    )
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class UserProfile(TimeStampedModel):
    """Extended user profile with weather preferences."""
    TEMP_UNITS = [('celsius', 'Celsius'), ('fahrenheit', 'Fahrenheit')]
    THEME_CHOICES = [('light', 'Light'), ('dark', 'Dark'), ('system', 'System')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.CharField(max_length=500, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Weather preferences
    temperature_unit = models.CharField(max_length=15, choices=TEMP_UNITS, default='celsius')
    wind_speed_unit = models.CharField(max_length=10, default='km/h')
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='system')

    # Notification preferences
    push_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    alert_notifications = models.BooleanField(default=True)
    daily_forecast_email = models.BooleanField(default=False)

    # AQI preferences
    aqi_alerts_enabled = models.BooleanField(default=True)
    aqi_threshold = models.IntegerField(default=100)

    # Premium
    is_premium = models.BooleanField(default=False)
    premium_expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"Profile: {self.user.email}"

    @property
    def is_premium_active(self):
        if not self.is_premium:
            return False
        if self.premium_expires_at and self.premium_expires_at < timezone.now():
            return False
        return True


class UserDevice(TimeStampedModel):
    """Track user device sessions for session management."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_name = models.CharField(max_length=255)
    device_type = models.CharField(
        max_length=20,
        choices=[('mobile', 'Mobile'), ('tablet', 'Tablet'), ('desktop', 'Desktop'), ('other', 'Other')],
        default='other',
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    last_active = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    fcm_token = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'user_devices'
        ordering = ['-last_active']

    def __str__(self):
        return f"{self.user.email} - {self.device_name}"


class OTPVerification(TimeStampedModel):
    """OTP codes for phone/email verification."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_codes', null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    otp_code = models.CharField(max_length=6)
    purpose = models.CharField(
        max_length=20,
        choices=[
            ('login', 'Login'),
            ('signup', 'Signup'),
            ('verify_email', 'Email Verification'),
            ('verify_phone', 'Phone Verification'),
            ('reset_password', 'Password Reset'),
        ],
    )
    is_used = models.BooleanField(default=False)
    expires_at = models.DateTimeField()
    attempts = models.IntegerField(default=0)

    class Meta:
        db_table = 'otp_verifications'
        ordering = ['-created_at']

    def is_expired(self):
        return timezone.now() > self.expires_at

    def is_valid(self):
        return not self.is_used and not self.is_expired() and self.attempts < 5
