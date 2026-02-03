"""Festival API views."""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q, Sum

from apps.festivals.models import Festival, FestivalStory, FestivalActivity, FestivalProgress
from apps.festivals.serializers import (
    FestivalSerializer,
    FestivalDetailSerializer,
    FestivalStorySerializer,
    FestivalActivitySerializer,
    FestivalProgressSerializer,
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

        # Annotate with counts
        queryset = queryset.annotate(
            total_activities=Count('activities', filter=Q(activities__is_active=True)),
            total_stories=Count('festival_stories')
        )

        # Ensure ordering by month (January to December)
        return queryset.order_by('typical_month', 'name')

    def get_serializer_context(self):
        """Add child language to context."""
        context = super().get_serializer_context()
        child_language = self.request.query_params.get('language')
        if child_language:
            context['child_language'] = child_language
        return context

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get festivals in the next 60 days based on typical month."""
        now = timezone.now()
        current_month = now.month
        next_month = (current_month % 12) + 1
        month_after = (next_month % 12) + 1

        # Get festivals for current, next, and month after
        festivals = self.get_queryset().filter(
            typical_month__in=[current_month, next_month, month_after]
        )

        serializer = self.get_serializer(festivals, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-religion')
    def by_religion(self, request):
        """Get festivals grouped by religion."""
        result = {}
        for religion_code, religion_name in Festival._meta.get_field('religion').choices:
            festivals = self.get_queryset().filter(religion=religion_code)
            result[religion_code] = {
                'name': religion_name,
                'count': festivals.count(),
                'festivals': FestivalSerializer(
                    festivals,
                    many=True,
                    context=self.get_serializer_context()
                ).data
            }
        return Response(result)

    @action(detail=True, methods=['get'])
    def stories(self, request, pk=None):
        """Get stories associated with a festival."""
        from apps.stories.serializers import StoryListSerializer

        festival = self.get_object()
        festival_stories = FestivalStory.objects.filter(
            festival=festival
        ).select_related('story')

        # Return flat Story objects instead of nested FestivalStory objects
        stories = [fs.story for fs in festival_stories if fs.story]
        serializer = StoryListSerializer(stories, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get activities for a festival, optionally filtered by age."""
        festival = self.get_object()
        activities = FestivalActivity.objects.filter(
            festival=festival,
            is_active=True
        )

        # Filter by age if provided
        age = request.query_params.get('age')
        context = {}
        if age:
            age = int(age)
            activities = activities.filter(
                min_age__lte=age,
                max_age__gte=age
            )
            context['child_age'] = age

        # Filter by activity type
        activity_type = request.query_params.get('type')
        if activity_type:
            activities = activities.filter(activity_type=activity_type.upper())

        serializer = FestivalActivitySerializer(
            activities,
            many=True,
            context=context
        )
        return Response(serializer.data)


class FestivalActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for FestivalActivity model."""

    queryset = FestivalActivity.objects.filter(is_active=True)
    serializer_class = FestivalActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by festival
        festival_id = self.request.query_params.get('festival')
        if festival_id:
            queryset = queryset.filter(festival_id=festival_id)

        # Filter by activity type
        activity_type = self.request.query_params.get('type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type.upper())

        # Filter by age appropriateness
        age = self.request.query_params.get('age')
        if age:
            age = int(age)
            queryset = queryset.filter(min_age__lte=age, max_age__gte=age)

        return queryset


class FestivalProgressViewSet(viewsets.ModelViewSet):
    """ViewSet for FestivalProgress model."""

    queryset = FestivalProgress.objects.all()
    serializer_class = FestivalProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Filter by child
        child_id = self.request.query_params.get('child')
        if child_id:
            queryset = queryset.filter(child_id=child_id)

        # Filter by festival
        festival_id = self.request.query_params.get('festival')
        if festival_id:
            queryset = queryset.filter(festival_id=festival_id)

        # Filter by completion status
        completed = self.request.query_params.get('completed')
        if completed is not None:
            is_completed = completed.lower() == 'true'
            queryset = queryset.filter(is_completed=is_completed)

        return queryset.select_related('child', 'festival', 'activity', 'story')

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """Mark a festival progress item as complete."""
        progress = self.get_object()
        points = progress.mark_complete()

        return Response({
            'message': 'Progress marked as complete',
            'points_earned': points,
            'progress': FestivalProgressSerializer(progress).data
        })

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get progress summary for a child."""
        child_id = request.query_params.get('child')
        if not child_id:
            return Response(
                {'error': 'child parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get all progress for child
        progress = FestivalProgress.objects.filter(child_id=child_id)

        # Calculate statistics
        total_items = progress.count()
        completed_items = progress.filter(is_completed=True).count()
        total_points = progress.filter(is_completed=True).aggregate(
            total=Sum('points_earned')
        )['total'] or 0

        # Get festival-wise breakdown
        festivals = progress.values('festival__name').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(is_completed=True))
        )

        return Response({
            'total_items': total_items,
            'completed_items': completed_items,
            'completion_rate': (completed_items / total_items * 100) if total_items > 0 else 0,
            'total_points': total_points,
            'festivals': list(festivals)
        })
