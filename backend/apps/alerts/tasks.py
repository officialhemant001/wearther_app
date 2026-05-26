from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.alerts.tasks.check_alert_conditions')
def check_alert_conditions():
    """Evaluate active alert rules against current weather conditions."""
    from .models import AlertRule, WeatherAlert
    from apps.weather.services import WeatherService
    from django.utils import timezone

    rules = AlertRule.objects.filter(is_active=True).select_related('user')
    weather_service = WeatherService()

    for rule in rules:
        try:
            weather = weather_service.get_current_weather(rule.latitude, rule.longitude)
            current_value = None

            if rule.metric == 'temperature':
                current_value = weather.get('temperature')
            elif rule.metric == 'humidity':
                current_value = weather.get('humidity')
            elif rule.metric == 'wind_speed':
                current_value = weather.get('wind_speed')

            if current_value is None:
                continue

            trigger = False
            if rule.condition == 'above' and current_value > rule.threshold:
                trigger = True
            elif rule.condition == 'below' and current_value < rule.threshold:
                trigger = True
            elif rule.condition == 'equals' and current_value == rule.threshold:
                trigger = True

            if trigger:
                # Trigger alert and save history
                WeatherAlert.objects.create(
                    user=rule.user,
                    rule=rule,
                    title=f"Alert: {rule.name}",
                    message=f"Weather condition met! {rule.metric} is {current_value}, which is {rule.condition} {rule.threshold}.",
                    severity='warning',
                    source='alert_engine',
                )
                rule.last_triggered_at = timezone.now()
                rule.save(update_fields=['last_triggered_at'])
                logger.info(f"Alert rule triggered: {rule.id}")

        except Exception as e:
            logger.error(f"Error checking alert rule {rule.id}: {e}")
