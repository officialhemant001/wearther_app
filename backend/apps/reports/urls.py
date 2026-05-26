from django.urls import path
from .views import WeatherReportView

app_name = 'reports'

urlpatterns = [
    path('generate/', WeatherReportView.as_view(), name='generate-report'),
]
