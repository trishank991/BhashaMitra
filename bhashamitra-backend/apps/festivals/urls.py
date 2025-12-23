"""Festival URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.festivals.views import FestivalViewSet, FestivalActivityViewSet, FestivalProgressViewSet

router = DefaultRouter()
router.register(r'festivals', FestivalViewSet, basename='festival')
router.register(r'festival-activities', FestivalActivityViewSet, basename='festival-activity')
router.register(r'festival-progress', FestivalProgressViewSet, basename='festival-progress')

urlpatterns = [
    path('', include(router.urls)),
]
