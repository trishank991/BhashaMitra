"""URL configuration for BhashaMitra project."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse


def health_check(request):
    """Simple health check endpoint."""
    return JsonResponse({'status': 'healthy', 'service': 'bhashamitra-api'})


urlpatterns = [
    path('', health_check, name='health'),
    path('health/', health_check, name='health-check'),
    path('admin/', admin.site.urls),

    # API v1
    path('api/v1/auth/', include('apps.users.urls', namespace='users')),
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
    path('api/v1/', include('apps.festivals.urls')),

    # Child-specific nested routes
    path('api/v1/children/<uuid:child_id>/progress/', include('apps.progress.urls', namespace='progress')),
    path('api/v1/children/<uuid:child_id>/', include('apps.gamification.urls', namespace='gamification')),
    path('api/v1/children/<uuid:child_id>/curriculum/', include('apps.curriculum.urls', namespace='curriculum')),
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
