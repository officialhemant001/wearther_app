from django.contrib import admin
from .models import AlertRule, WeatherAlert


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'metric', 'condition', 'threshold', 'is_active']
    list_filter = ['metric', 'is_active']


@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'severity', 'is_read', 'created_at']
    list_filter = ['severity', 'is_read']
