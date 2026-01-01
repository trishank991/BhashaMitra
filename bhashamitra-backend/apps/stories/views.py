"""Story views."""
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Story
from .serializers import StoryListSerializer, StoryDetailSerializer
from apps.core.validators import safe_limit


class StoryListView(APIView):
    """List stories with filters and tier-based access."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        language = request.query_params.get('language')
        level = request.query_params.get('level')
        tier = request.query_params.get('tier')
        limit = safe_limit(request.query_params.get('limit'), default=50, max_limit=100)

        if not language:
            return Response(
                {'detail': 'language parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user's subscription tier
        user_tier = getattr(request.user, 'subscription_tier', 'FREE')
        user_story_limit = getattr(request.user, 'story_limit', 5)

        # Base queryset - only active stories
        queryset = Story.objects.filter(language=language, is_active=True)

        # Filter by tier based on user's subscription
        # FREE users can only see free stories
        # STANDARD/PREMIUM users can see all stories up to their tier
        # Note: Use case-insensitive filtering since tier values may be 'free' or 'FREE'
        user_tier_lower = user_tier.lower() if user_tier else 'free'
        if user_tier_lower == 'free':
            queryset = queryset.filter(tier__iexact='free')
        elif user_tier_lower == 'standard':
            queryset = queryset.filter(tier__iregex=r'^(free|standard)$')
        # PREMIUM users see all stories (no filter needed)

        # Additional filters
        if level:
            queryset = queryset.filter(level=level)
        if tier:
            queryset = queryset.filter(tier=tier)

        # Order by sort_order and then by featured
        queryset = queryset.order_by('-is_featured', 'sort_order', 'title_hindi')

        # Apply limit based on user's tier
        total_available = queryset.count()
        if user_story_limit != -1:
            effective_limit = min(limit, user_story_limit)
        else:
            effective_limit = limit
        stories = queryset[:effective_limit]

        serializer = StoryListSerializer(stories, many=True)

        return Response({
            'data': serializer.data,
            'meta': {
                'total': len(serializer.data),
                'total_available': total_available,
                'user_story_limit': user_story_limit,
                'is_limited': user_story_limit != -1 and total_available > user_story_limit,
                'subscription_tier': user_tier,
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
