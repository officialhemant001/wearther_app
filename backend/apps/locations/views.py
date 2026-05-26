from rest_framework import viewsets
from .models import SavedLocation
from .serializers import SavedLocationSerializer


class SavedLocationViewSet(viewsets.ModelViewSet):
    """Manage saved locations."""
    serializer_class = SavedLocationSerializer

    def get_queryset(self):
        return SavedLocation.objects.filter(user=self.request.user, is_active=True)
