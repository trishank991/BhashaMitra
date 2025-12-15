"""Custom exception handling."""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """Custom exception handler following RFC 7807."""
    response = exception_handler(exc, context)

    if response is None:
        logger.exception("Unhandled exception", exc_info=exc)
        return Response(
            {
                'type': 'https://bhashamitra.co.nz/errors/internal',
                'title': 'Internal Server Error',
                'status': 500,
                'detail': 'An unexpected error occurred.',
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    error_types = {
        400: 'validation',
        401: 'unauthorized',
        403: 'forbidden',
        404: 'not-found',
        405: 'method-not-allowed',
        409: 'conflict',
        429: 'rate-limited',
        500: 'internal',
        503: 'unavailable',
    }

    error_titles = {
        400: 'Validation Error',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        405: 'Method Not Allowed',
        409: 'Conflict',
        429: 'Rate Limited',
        500: 'Internal Server Error',
        503: 'Service Unavailable',
    }

    error_response = {
        'type': f'https://bhashamitra.co.nz/errors/{error_types.get(response.status_code, "error")}',
        'title': error_titles.get(response.status_code, 'Error'),
        'status': response.status_code,
        'detail': _extract_detail(response.data),
    }

    response.data = error_response
    return response


def _extract_detail(data):
    """Extract error detail from response data."""
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        if 'non_field_errors' in data:
            return data['non_field_errors'][0]
        for key, value in data.items():
            if isinstance(value, list):
                return f"{key}: {value[0]}"
            return f"{key}: {value}"
    if isinstance(data, list):
        return data[0] if data else 'An error occurred'
    return str(data)


class AppException(Exception):
    """Base exception for application errors."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_message = 'An error occurred'

    def __init__(self, message=None, code=None):
        self.message = message or self.default_message
        self.code = code


class NotFoundError(AppException):
    status_code = status.HTTP_404_NOT_FOUND
    default_message = 'Resource not found'


class ValidationError(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_message = 'Validation error'
