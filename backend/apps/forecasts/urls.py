from django.urls import path
from .views import ForecastView

app_name = 'forecasts'

urlpatterns = [
    path('', ForecastView.as_view(), name='forecast'),
]
