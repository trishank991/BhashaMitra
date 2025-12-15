"""Progress views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from apps.children.models import Child
from apps.stories.models import Story
from .models import Progress
from .services import ProgressService


class ProgressListView(APIView):
    """List progress records for a child."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        status_filter = request.query_params.get('status')
        queryset = Progress.objects.filter(child=child).select_related('story')

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        data = [{
            'id': p.id,
            'story_id': p.story_id,
            'story_title': p.story.title,
            'status': p.status,
            'current_page': p.current_page,
            'total_pages': p.story.page_count,
            'last_read_at': p.last_read_at,
        } for p in queryset]

        return Response({'data': data})


class ProgressActionView(APIView):
    """Handle progress actions."""
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id):
        try:
            child = Child.objects.get(pk=child_id, user=request.user)
        except Child.DoesNotExist:
            return Response({'detail': 'Child not found'}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')
        story_id = request.data.get('story_id')

        if action == 'start':
            try:
                story = Story.objects.get(pk=story_id)
            except Story.DoesNotExist:
                return Response({'detail': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)

            progress = ProgressService.start_story(child, story)
            return Response({'data': {'id': progress.id, 'status': progress.status}})

        elif action == 'update':
            try:
                progress = Progress.objects.get(child=child, story_id=story_id)
            except Progress.DoesNotExist:
                return Response({'detail': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)

            progress = ProgressService.update_progress(
                progress,
                request.data.get('current_page', 0),
                request.data.get('time_spent_seconds', 0)
            )
            return Response({'data': {'id': progress.id, 'current_page': progress.current_page}})

        elif action == 'complete':
            try:
                progress = Progress.objects.get(child=child, story_id=story_id)
            except Progress.DoesNotExist:
                return Response({'detail': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)

            result = ProgressService.complete_story(
                progress, request.data.get('time_spent_seconds', 0)
            )
            return Response({
                'data': {'id': result['progress'].id, 'status': 'COMPLETED'},
                'meta': {
                    'points_awarded': result['points_awarded'],
                    'new_badges': [b.badge.name for b in result['new_badges']],
                    'level_up': result['level_up'],
                }
            })

        return Response({'detail': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
