from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.core.utils import success_response
from .models import AlertRule, WeatherAlert
from .serializers import AlertRuleSerializer, WeatherAlertSerializer


class AlertRuleViewSet(viewsets.ModelViewSet):
    """Manage custom alert rules."""
    serializer_class = AlertRuleSerializer

    def get_queryset(self):
        return AlertRule.objects.filter(user=self.request.user)


class WeatherAlertViewSet(viewsets.ReadOnlyModelViewSet):
    """View and toggle read status of weather alerts."""
    serializer_class = WeatherAlertSerializer

    def get_queryset(self):
        return WeatherAlert.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        alert = self.get_object()
        alert.is_read = True
        alert.save(update_fields=['is_read', 'updated_at'])
        return Response(success_response(message='Alert marked as read.'))

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response(success_response(message='All alerts marked as read.'))
