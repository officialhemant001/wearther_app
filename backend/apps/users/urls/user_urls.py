"""
User profile and settings URL patterns.
"""

from django.urls import path
from apps.users.views import (
    UserProfileView, UserSettingsView,
    UserDeviceListView, UserDeviceDeleteView,
)

app_name = 'users'

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('devices/', UserDeviceListView.as_view(), name='device-list'),
    path('devices/<int:pk>/', UserDeviceDeleteView.as_view(), name='device-delete'),
]
