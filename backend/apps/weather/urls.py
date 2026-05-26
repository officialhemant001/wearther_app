from django.urls import path
from .views import CurrentWeatherView, HyperlocalWeatherView, WeatherSearchView

app_name = 'weather'

urlpatterns = [
    path('current/', CurrentWeatherView.as_view(), name='current'),
    path('hyperlocal/', HyperlocalWeatherView.as_view(), name='hyperlocal'),
    path('search/', WeatherSearchView.as_view(), name='search'),
]
