"""Festival API views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta

from apps.festivals.models import Festival, FestivalStory
from apps.festivals.serializers import (
    FestivalSerializer,
    FestivalDetailSerializer,
    FestivalStorySerializer,
)


class FestivalViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Festival model."""

    queryset = Festival.objects.filter(is_active=True)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return FestivalDetailSerializer
        return FestivalSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by religion
        religion = self.request.query_params.get('religion')
        if religion:
            queryset = queryset.filter(religion=religion.upper())

        # Filter by month
        month = self.request.query_params.get('month')
        if month:
            queryset = queryset.filter(typical_month=int(month))

        return queryset

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get festivals in the next 30 days based on typical month."""
        now = timezone.now()
        current_month = now.month

        # Get festivals for current and next month
        next_month = (current_month % 12) + 1
        festivals = self.get_queryset().filter(
            typical_month__in=[current_month, next_month]
        )

        serializer = self.get_serializer(festivals, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        """Get stories associated with a festival."""
        festival = self.get_object()
        festival_stories = FestivalStory.objects.filter(
            festival=festival
        ).select_related('story')

        serializer = FestivalStorySerializer(festival_stories, many=True)
        return Response(serializer.data)
