"""
Custom authentication backends.
"""

from django.contrib.auth.backends import ModelBackend
from .models import User


class EmailBackend(ModelBackend):
    """Authenticate using email instead of username."""
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Also support 'username' kwarg for compatibility
        if email is None:
            email = kwargs.get('username')
        if email is None:
            return None
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None


class PhoneBackend(ModelBackend):
    """Authenticate using phone number (OTP-based)."""
    def authenticate(self, request, phone_number=None, **kwargs):
        if phone_number is None:
            return None
        try:
            return User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return None
