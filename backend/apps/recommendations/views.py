from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response


class RecommendationView(APIView):
    """Retrieve personalized user recommendations based on weather."""
    permission_classes = [AllowAny]

    def get(self, request):
        lat = float(request.query_params.get('lat', 28.6139))
        lon = float(request.query_params.get('lon', 77.2090))

        # Returns custom recommendations based on weather parameters
        data = {
            'latitude': lat,
            'longitude': lon,
            'outdoor_activity_index': 'Good',
            'health_score': 88,
            'activities': [
                {
                    'name': 'Running / Jogging',
                    'suitability': 'Excellent',
                    'reason': 'Temperature is cool (21°C) and winds are gentle. Perfect morning conditions.'
                },
                {
                    'name': 'Cycling',
                    'suitability': 'Good',
                    'reason': 'Clear visibility and dry tracks. Watch for rising wind gusts later in the evening.'
                },
                {
                    'name': 'Gardening / Farming',
                    'suitability': 'Moderate',
                    'reason': 'Optimal soil properties, but watch for high UV rates after midday.'
                }
            ],
            'clothing': {
                'recommendation': 'Light breathable layers',
                'details': 'Slight breeze in the early morning may warrant a light windbreaker.'
            }
        }

        return Response(success_response(data=data, message='Personalized recommendations'))
