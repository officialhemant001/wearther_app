from django.urls import path
from .views import HealthWeatherView

app_name = 'health_weather'

urlpatterns = [
    path('', HealthWeatherView.as_view(), name='health-weather'),
]
