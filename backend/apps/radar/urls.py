from django.urls import path
from .views import RadarFrameView

app_name = 'radar'

urlpatterns = [
    path('frames/', RadarFrameView.as_view(), name='radar-frames'),
]
