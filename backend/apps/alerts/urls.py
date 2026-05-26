from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertRuleViewSet, WeatherAlertViewSet

app_name = 'alerts'

router = DefaultRouter()
router.register('rules', AlertRuleViewSet, basename='rule')
router.register('history', WeatherAlertViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
]
