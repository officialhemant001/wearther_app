from django.contrib import admin
from .models import SavedLocation


@admin.register(SavedLocation)
class SavedLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'latitude', 'longitude', 'is_active']
    list_filter = ['is_active', 'country']
    search_fields = ['name']
