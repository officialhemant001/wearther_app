"""
Root URL configuration for Weather Application.
All API endpoints are versioned under /api/v1/.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.users.urls.auth_urls')),
    path('api/v1/users/', include('apps.users.urls.user_urls')),
    path('api/v1/weather/', include('apps.weather.urls')),
    path('api/v1/forecasts/', include('apps.forecasts.urls')),
    path('api/v1/alerts/', include('apps.alerts.urls')),
    path('api/v1/ai/', include('apps.ai_engine.urls')),
    path('api/v1/radar/', include('apps.radar.urls')),
    path('api/v1/locations/', include('apps.locations.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/subscriptions/', include('apps.subscriptions.urls')),
    path('api/v1/settings/', include('apps.settings_manager.urls')),
    path('api/v1/recommendations/', include('apps.recommendations.urls')),
    path('api/v1/health/', include('apps.health_weather.urls')),
    path('api/v1/farming/', include('apps.farming_weather.urls')),
    path('api/v1/reports/', include('apps.reports.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
