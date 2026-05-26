"""
Custom exception handler for DRF.
Provides consistent error response format across the API.
"""

from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.core.exceptions import ValidationError as DjangoValidationError


def custom_exception_handler(exc, context):
    """
    Returns consistent error responses:
    {
        "success": false,
        "error": {
            "code": "ERROR_CODE",
            "message": "Human-readable message",
            "details": {}
        }
    }
    """
    # Call DRF's default handler first
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'error': {
                'code': _get_error_code(response.status_code),
                'message': _get_error_message(exc, response),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
            }
        }
        response.data = error_data
        return response

    # Handle Django ValidationError
    if isinstance(exc, DjangoValidationError):
        return Response({
            'success': False,
            'error': {
                'code': 'VALIDATION_ERROR',
                'message': 'Validation failed.',
                'details': exc.message_dict if hasattr(exc, 'message_dict') else {'detail': exc.messages},
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    return None


def _get_error_code(status_code):
    codes = {
        400: 'BAD_REQUEST',
        401: 'UNAUTHORIZED',
        403: 'FORBIDDEN',
        404: 'NOT_FOUND',
        405: 'METHOD_NOT_ALLOWED',
        429: 'THROTTLED',
        500: 'INTERNAL_ERROR',
    }
    return codes.get(status_code, 'ERROR')


def _get_error_message(exc, response):
    if hasattr(exc, 'detail'):
        if isinstance(exc.detail, str):
            return exc.detail
        if isinstance(exc.detail, list):
            return exc.detail[0] if exc.detail else 'An error occurred.'
    return 'An error occurred.'
