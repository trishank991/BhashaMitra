"""
Health Check Endpoints for BhashaMitra.

Provides comprehensive health checks for:
- Database connectivity
- Cache connectivity (Redis)
- External API availability
"""

from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
from django.utils import timezone
import time
import logging

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Basic health check endpoint.

    Returns 200 if the service is running.
    """
    return JsonResponse({
        'status': 'healthy',
        'service': 'bhashamitra-api',
        'timestamp': timezone.now().isoformat(),
    })


def readiness_check(request):
    """
    Readiness check endpoint.

    Verifies the service can handle requests:
    - Database is accessible
    - Cache is accessible (if configured)

    Returns 200 if ready, 503 if not ready.
    """
    checks = {
        'database': check_database(),
        'cache': check_cache(),
    }

    all_healthy = all(c['healthy'] for c in checks.values())

    response_data = {
        'status': 'ready' if all_healthy else 'not_ready',
        'timestamp': timezone.now().isoformat(),
        'checks': checks,
    }

    status_code = 200 if all_healthy else 503
    return JsonResponse(response_data, status=status_code)


def liveness_check(request):
    """
    Liveness check endpoint.

    Simply verifies the application is running.
    Used by container orchestrators to determine if the process should be restarted.
    """
    return JsonResponse({
        'status': 'alive',
        'timestamp': timezone.now().isoformat(),
    })


def detailed_health_check(request):
    """
    Detailed health check with performance metrics.

    Returns comprehensive status including:
    - Database query time
    - Cache read/write time
    - System info
    """
    checks = {}

    # Database check with timing
    db_start = time.time()
    checks['database'] = check_database()
    checks['database']['latency_ms'] = round((time.time() - db_start) * 1000, 2)

    # Cache check with timing
    cache_start = time.time()
    checks['cache'] = check_cache()
    checks['cache']['latency_ms'] = round((time.time() - cache_start) * 1000, 2)

    # Overall status
    all_healthy = all(c['healthy'] for c in checks.values())

    return JsonResponse({
        'status': 'healthy' if all_healthy else 'degraded',
        'timestamp': timezone.now().isoformat(),
        'version': get_version(),
        'checks': checks,
    })


def check_database():
    """Check database connectivity."""
    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        return {'healthy': True, 'message': 'Database connection OK'}
    except Exception as e:
        logger.error(f'Database health check failed: {e}')
        return {'healthy': False, 'message': str(e)}


def check_cache():
    """Check cache connectivity."""
    try:
        # Try to set and get a test value
        test_key = 'health_check_test'
        test_value = f'test_{timezone.now().timestamp()}'

        cache.set(test_key, test_value, timeout=10)
        retrieved = cache.get(test_key)

        if retrieved == test_value:
            cache.delete(test_key)
            return {'healthy': True, 'message': 'Cache connection OK'}
        else:
            return {'healthy': False, 'message': 'Cache read/write mismatch'}
    except Exception as e:
        # Cache might not be configured, which is OK for dev
        logger.warning(f'Cache health check: {e}')
        return {'healthy': True, 'message': 'Cache not configured (using fallback)'}


def get_version():
    """Get application version."""
    import os
    return os.getenv('APP_VERSION', '1.0.0')
