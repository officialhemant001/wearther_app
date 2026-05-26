from django.urls import path
from .views import AppSettingsView

app_name = 'settings_manager'

urlpatterns = [
    path('config/', AppSettingsView.as_view(), name='app-config'),
]
