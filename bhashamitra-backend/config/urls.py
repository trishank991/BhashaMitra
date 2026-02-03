from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from contextlib import suppress # Sourcery recommendation

from apps.core.health import (
    health_check,
    readiness_check,
    liveness_check,
    detailed_health_check,
)

urlpatterns = [
    # Health check endpoints
    path('', health_check, name='health'),
    path('health/', health_check, name='health-check'),
    path('health/ready/', readiness_check, name='readiness-check'),
    path('health/live/', liveness_check, name='liveness-check'),
    path('health/detailed/', detailed_health_check, name='detailed-health'),

    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.users.urls', namespace='users')),
    path('api/v1/challenges/', include('apps.challenges.urls', namespace='challenges')),
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/children/<uuid:child_id>/peppi-chat/', include('apps.peppi_chat.urls', namespace='peppi_chat')),
    path('api/v1/children/<uuid:child_id>/progress/', include('apps.progress.urls', namespace='progress')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
    path('api/v1/peppi/', include('apps.speech.peppi_urls', namespace='peppi')),
    path('api/v1/festivals/', include('apps.festivals.urls')),
    path('api/v1/curriculum/', include('apps.curriculum.urls', namespace='curriculum-global')),
    path('api/v1/parent/', include('apps.parent_engagement.urls', namespace='parent_engagement')),
    path('api/v1/family/', include('apps.family.urls', namespace='family')),
    path('api/v1/payments/', include('apps.payments.urls', namespace='payments')),
]

# Debug toolbar (development only)
if settings.DEBUG:
    with suppress(ImportError):
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)