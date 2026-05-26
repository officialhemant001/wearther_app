from rest_framework import serializers
from .models import SavedLocation


class SavedLocationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = SavedLocation
        fields = '__all__'
