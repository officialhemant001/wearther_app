from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response, timezone
from datetime import timedelta


class RadarFrameView(APIView):
    """Get recent radar tile frames (clouds/precipitation)."""
    permission_classes = [AllowAny]

    def get(self, request):
        # Generates a list of recent frames/tiles maps for visualization
        # In a real environment, this links to Mapbox, OpenWeatherMap or custom Tile Servers
        import random
        from django.utils import timezone

        layer = request.query_params.get('layer', 'precipitation')
        now = timezone.now()
        frames = []

        # Return simulated tiles for the past 6 frames (last 2 hours, 20 min interval)
        for i in range(6):
            time = now - timedelta(minutes=20 * i)
            frames.append({
                'timestamp': time.isoformat(),
                # OpenWeatherMap tile server URL structure
                'tile_url': f"https://tile.openweathermap.org/map/{layer}_new/{{z}}/{{x}}/{{y}}.png?appid=demo",
                'description': f"Radar layer {layer} at {time.strftime('%H:%M')}"
            })

        return Response(success_response(data=frames, message='Recent radar frames'))
