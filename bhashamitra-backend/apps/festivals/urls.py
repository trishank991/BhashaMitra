"""Festival URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.festivals.views import FestivalViewSet

router = DefaultRouter()
router.register(r'festivals', FestivalViewSet, basename='festival')

urlpatterns = [
    path('', include(router.urls)),
]
