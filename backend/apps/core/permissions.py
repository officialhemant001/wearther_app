"""
Core permissions used across all apps.
"""

from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Object-level permission: only the owner can access."""
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False


class IsPremiumUser(BasePermission):
    """Only premium subscribers can access."""
    message = 'Premium subscription required.'

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.is_premium
        )


class IsAdminOrReadOnly(BasePermission):
    """Admin can write; others read-only."""
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return request.user and request.user.is_staff
