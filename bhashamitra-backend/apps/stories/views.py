"""Story views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Story
from .serializers import StoryListSerializer, StoryDetailSerializer


class StoryListView(APIView):
    """List stories with filters and tier-based limits."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        language = request.query_params.get('language')
        level = request.query_params.get('level')
        limit = int(request.query_params.get('limit', 20))

        if not language:
            return Response(
                {'detail': 'language parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user's story limit based on subscription tier
        # FREE: 4, STANDARD: 8, PREMIUM: unlimited (9999)
        user_story_limit = getattr(request.user, 'story_limit', 4)

        queryset = Story.objects.filter(language=language)
        if level:
            queryset = queryset.filter(level=level)

        # Apply the more restrictive limit (user's tier limit or requested limit)
        effective_limit = min(limit, user_story_limit)
        stories = queryset[:effective_limit]
        total_available = queryset.count()

        serializer = StoryListSerializer(stories, many=True)

        return Response({
            'data': serializer.data,
            'meta': {
                'total': len(serializer.data),
                'total_available': total_available,
                'user_story_limit': user_story_limit,
                'is_limited': total_available > user_story_limit,
                'subscription_tier': getattr(request.user, 'subscription_tier', 'FREE'),
            }
        })


class StoryDetailView(APIView):
    """Get story with pages."""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            story = Story.objects.prefetch_related('pages').get(pk=pk)
        except Story.DoesNotExist:
            return Response({'detail': 'Story not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StoryDetailSerializer(story)
        return Response({'data': serializer.data})
