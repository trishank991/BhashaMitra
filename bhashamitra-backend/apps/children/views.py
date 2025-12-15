"""Child views."""
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

from apps.core.permissions import IsParentOfChild
from .models import Child
from .serializers import (
    ChildSerializer,
    CreateChildSerializer,
    UpdateChildSerializer,
    ChildStatsSerializer,
)


class ChildListCreateView(generics.ListCreateAPIView):
    """List and create children for the authenticated parent."""
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateChildSerializer
        return ChildSerializer


class ChildDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a child profile."""
    permission_classes = [IsAuthenticated, IsParentOfChild]

    def get_queryset(self):
        return Child.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateChildSerializer
        return ChildSerializer

    def perform_destroy(self, instance):
        instance.soft_delete()


class ChildStatsView(APIView):
    """Get child statistics for a given period."""
    permission_classes = [IsAuthenticated, IsParentOfChild]

    def get(self, request, pk):
        try:
            child = Child.objects.get(pk=pk, user=request.user)
        except Child.DoesNotExist:
            return Response(
                {'detail': 'Child not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        period = request.query_params.get('period', 'week')

        # Calculate date range
        today = timezone.now().date()
        if period == 'day':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        else:
            start_date = None  # All time

        # Get daily activities
        from apps.progress.models import DailyActivity
        activities = DailyActivity.objects.filter(child=child)
        if start_date:
            activities = activities.filter(date__gte=start_date)

        # Aggregate stats
        stats = activities.aggregate(
            stories_started=Sum('stories_started'),
            stories_completed=Sum('stories_completed'),
            pages_read=Sum('pages_read'),
            time_spent_seconds=Sum('time_spent_seconds'),
            points_earned=Sum('points_earned'),
            recordings_made=Sum('recordings_made'),
        )

        # Get streak and badges
        from apps.gamification.models import Streak, ChildBadge
        streak = Streak.objects.filter(child=child).first()
        badges_count = ChildBadge.objects.filter(child=child).count()

        response_data = {
            'child_id': child.id,
            'period': period,
            'stories_started': stats['stories_started'] or 0,
            'stories_completed': stats['stories_completed'] or 0,
            'pages_read': stats['pages_read'] or 0,
            'time_spent_minutes': (stats['time_spent_seconds'] or 0) // 60,
            'points_earned': stats['points_earned'] or 0,
            'recordings_made': stats['recordings_made'] or 0,
            'current_streak': streak.current_streak if streak else 0,
            'badges_earned': badges_count,
        }

        return Response({'data': response_data})
