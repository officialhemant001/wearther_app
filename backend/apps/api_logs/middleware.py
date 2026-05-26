"""
API request/response logger middleware.
"""

import time
import logging
from django.utils.deprecation import MiddlewareMixin
from apps.core.utils import get_client_ip, get_user_agent

logger = logging.getLogger('apps.api_logs')


class APILogMiddleware(MiddlewareMixin):
    """Logs API requests and execution times."""
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if not request.path.startswith('/api/'):
            return response

        duration = 0.0
        if hasattr(request, 'start_time'):
            duration = time.time() - request.start_time

        ip = get_client_ip(request)
        ua = get_user_agent(request)
        user = request.user if request.user.is_authenticated else 'Anonymous'

        logger.info(
            f"User={user} IP={ip} Method={request.method} Path={request.path} "
            f"Status={response.status_code} Duration={duration:.3f}s UA={ua}"
        )

        return response
