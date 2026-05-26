"""
Core utility functions.
"""

import random
import string
from django.utils import timezone


def generate_otp(length=6):
    """Generate a numeric OTP code."""
    return ''.join(random.choices(string.digits, k=length))


def get_client_ip(request):
    """Extract client IP from request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')


def get_user_agent(request):
    """Extract user agent from request."""
    return request.META.get('HTTP_USER_AGENT', 'Unknown')


def success_response(data=None, message='Success', status_code=200):
    """Standard success response format."""
    response = {
        'success': True,
        'message': message,
    }
    if data is not None:
        response['data'] = data
    return response
