from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(name='apps.weather.tasks.fetch_weather_data_periodic')
def fetch_weather_data_periodic():
    """Periodically fetch weather data for all saved locations."""
    from apps.locations.models import SavedLocation
    from .services import WeatherService

    service = WeatherService()
    locations = SavedLocation.objects.filter(is_active=True).select_related('user')

    for loc in locations:
        try:
            service.get_current_weather(loc.latitude, loc.longitude)
            logger.info(f"Fetched weather for {loc.name}")
        except Exception as e:
            logger.error(f"Failed to fetch weather for {loc.name}: {e}")
