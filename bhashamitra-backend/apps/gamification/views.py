"""Gamification views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from .services.badges import BadgeService
from .services.streaks import StreakService
from .services.levels import LevelService
from .models import VoiceRecording


class BadgeListView(APIView):
    """Get badges for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        badges = BadgeService.get_badges_for_child(child)
        return Response({'data': badges})


class StreakView(APIView):
    """Get streak for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        streak = StreakService.get_streak(child)
        return Response({'data': streak})


class LevelView(APIView):
    """Get level progress for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        level_info = LevelService.get_level_progress(child)
        return Response({'data': level_info})


class RecordingListView(APIView):
    """List and create voice recordings."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        recordings = VoiceRecording.objects.filter(child=child).order_by('-recorded_at')[:20]

        data = [{
            'id': r.id,
            'story_id': r.story_id,
            'page_number': r.page_number,
            'audio_url': r.audio_url,
            'duration_ms': r.duration_ms,
            'recorded_at': r.recorded_at,
        } for r in recordings]

        return Response({'data': data})

    def post(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        recording = VoiceRecording.objects.create(
            child=child,
            story_id=request.data.get('story_id'),
            page_number=request.data.get('page_number'),
            audio_url=request.data.get('audio_url'),
            duration_ms=request.data.get('duration_ms', 0),
        )

        # Award points
        from django.conf import settings
        points = settings.POINTS_CONFIG['VOICE_RECORDING']
        child.total_points += points
        child.save(update_fields=['total_points'])

        return Response({
            'data': {'id': recording.id},
            'meta': {'points_awarded': points}
        }, status=status.HTTP_201_CREATED)
