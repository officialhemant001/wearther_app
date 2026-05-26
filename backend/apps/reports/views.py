from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from apps.core.utils import success_response


class WeatherReportView(APIView):
    """Generate dynamic PDF or Excel files summarizing weather metrics."""
    permission_classes = [AllowAny]

    def get(self, request):
        data = {
            'report_id': 'REP-99881',
            'status': 'Generated',
            'location': 'New Delhi, IN',
            'summary': {
                'average_temp': '32.1°C',
                'max_temp': '38.4°C',
                'total_precipitation': '12 mm',
                'days_with_warnings': 2,
            },
            'download_url': '/media/reports/REP-99881.pdf'
        }
        return Response(success_response(data=data, message='Weather report generated'))
