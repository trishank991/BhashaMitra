"""URL configuration for BhashaMitra project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

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
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
    path('api/v1/peppi/', include('apps.speech.peppi_urls', namespace='peppi')),
    path('api/v1/festivals/', include('apps.festivals.urls')),
    path('api/v1/curriculum/', include('apps.curriculum.urls', namespace='curriculum-global')),

    # Parent dashboard API
    path('api/v1/parent/', include('apps.parent_engagement.urls', namespace='parent_engagement')),

    # Child-specific nested routes
    path('api/v1/children/<uuid:child_id>/progress/', include('apps.progress.urls', namespace='progress')),
    path('api/v1/children/<uuid:child_id>/', include('apps.gamification.urls', namespace='gamification')),
    path('api/v1/children/<uuid:child_id>/curriculum/', include('apps.curriculum.urls', namespace='curriculum-child')),
    path('api/v1/children/<uuid:child_id>/mimic/', include('apps.speech.mimic_urls', namespace='mimic')),
    path('api/v1/children/<uuid:child_id>/peppi-chat/', include('apps.peppi_chat.urls', namespace='peppi_chat')),
]

# Debug toolbar (development only)
if settings.DEBUG:
    try:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
    except ImportError:
        pass

    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
