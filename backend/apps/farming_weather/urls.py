from django.urls import path
from .views import FarmingWeatherView

app_name = 'farming_weather'

urlpatterns = [
    path('', FarmingWeatherView.as_view(), name='farming-weather'),
]
