"""
Challenge API Views.

Public endpoints (AllowAny - for viral sharing):
- GET  /api/v1/challenges/play/<code>/     - Get challenge to play
- POST /api/v1/challenges/play/<code>/     - Start attempt (get attempt_id)
- POST /api/v1/challenges/submit/          - Submit answers
- GET  /api/v1/challenges/leaderboard/<code>/ - Get leaderboard

Authenticated endpoints:
- GET  /api/v1/challenges/                 - List my challenges
- POST /api/v1/challenges/                 - Create challenge
- GET  /api/v1/challenges/<code>/          - Get my challenge details
- GET  /api/v1/challenges/quota/           - Get my quota
- GET  /api/v1/challenges/categories/      - Get available categories
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from .models import Challenge, ChallengeAttempt, UserChallengeQuota
from .serializers import (
    ChallengeCreateSerializer, ChallengeSerializer, PublicChallengeSerializer,
    ChallengeAttemptCreateSerializer, ChallengeSubmitSerializer,
    ChallengeAttemptSerializer, LeaderboardEntrySerializer,
    QuotaSerializer, CategorySerializer
)
from .services import ChallengeService


# =============================================================================
# PUBLIC ENDPOINTS - No authentication required
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def play_challenge(request, code):
    """
    GET: Get challenge info for playing (questions without answers)
    POST: Start a new attempt (returns attempt_id)
    """
    challenge = get_object_or_404(Challenge, code=code.upper(), is_active=True)

    # Check if expired
    if challenge.is_expired:
        return Response(
            {"error": "This challenge has expired", "expired": True},
            status=status.HTTP_410_GONE
        )

    if request.method == 'GET':
        serializer = PublicChallengeSerializer(challenge)
        return Response({
            "success": True,
            "data": serializer.data
        })

    elif request.method == 'POST':
        serializer = ChallengeAttemptCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create attempt
        attempt = ChallengeAttempt.objects.create(
            challenge=challenge,
            participant_name=serializer.validated_data['participant_name'],
            participant_location=serializer.validated_data.get('participant_location', ''),
            max_score=challenge.question_count,
            # Link to authenticated user if logged in
            participant_user=request.user if request.user.is_authenticated else None,
        )

        # Increment attempt count
        challenge.total_attempts += 1
        challenge.save(update_fields=['total_attempts'])

        return Response({
            "success": True,
            "data": {
                "attempt_id": str(attempt.id),
                "challenge": PublicChallengeSerializer(challenge).data
            }
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_challenge(request):
    """Submit answers and get results."""
    serializer = ChallengeSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    attempt_id = serializer.validated_data['attempt_id']
    answers = serializer.validated_data['answers']
    time_taken = serializer.validated_data['time_taken_seconds']

    # Get attempt
    try:
        attempt = ChallengeAttempt.objects.select_related('challenge').get(id=attempt_id)
    except ChallengeAttempt.DoesNotExist:
        return Response(
            {"success": False, "error": "Attempt not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if already completed
    if attempt.is_completed:
        return Response(
            {"success": False, "error": "This attempt was already submitted"},
            status=status.HTTP_400_BAD_REQUEST
        )

    challenge = attempt.challenge

    # Calculate score
    try:
        result = ChallengeService.calculate_score(challenge.questions, answers)
    except ValueError as e:
        return Response(
            {"success": False, "error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update attempt
    with transaction.atomic():
        attempt.score = result['score']
        attempt.percentage = result['percentage']
        attempt.time_taken_seconds = time_taken
        attempt.answers = result['detailed_results']
        attempt.is_completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        # Update challenge stats
        challenge.total_completions += 1
        # Recalculate average score
        completed_attempts = ChallengeAttempt.objects.filter(
            challenge=challenge,
            is_completed=True
        )
        total_percentage = sum(a.percentage for a in completed_attempts)
        challenge.average_score = total_percentage / challenge.total_completions
        challenge.save(update_fields=['total_completions', 'average_score'])

    # Get rank
    rank = attempt.rank

    return Response({
        "success": True,
        "data": {
            "score": result['score'],
            "max_score": result['max_score'],
            "percentage": result['percentage'],
            "time_taken_seconds": time_taken,
            "rank": rank,
            "total_participants": challenge.total_completions,
            "detailed_results": result['detailed_results'],
            "challenge_title": challenge.title,
            "share_url": challenge.share_url,
        }
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def challenge_leaderboard(request, code):
    """Get leaderboard for a challenge."""
    challenge = get_object_or_404(Challenge, code=code.upper())

    # Get top 20 completed attempts
    attempts = ChallengeAttempt.objects.filter(
        challenge=challenge,
        is_completed=True
    ).order_by('-percentage', 'time_taken_seconds')[:20]

    serializer = LeaderboardEntrySerializer(attempts, many=True)

    return Response({
        "success": True,
        "data": {
            "challenge_title": challenge.title,
            "challenge_code": challenge.code,
            "total_participants": challenge.total_completions,
            "average_score": round(challenge.average_score, 1),
            "leaderboard": serializer.data,
        }
    })


# =============================================================================
# AUTHENTICATED ENDPOINTS - Creator only
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def challenges_list_create(request):
    """
    GET: List user's created challenges
    POST: Create a new challenge
    """
    user = request.user

    if request.method == 'GET':
        challenges = Challenge.objects.filter(creator=user).order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    elif request.method == 'POST':
        serializer = ChallengeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check quota
        quota, _ = UserChallengeQuota.objects.get_or_create(user=user)
        is_paid = user.is_premium_tier or user.is_standard_tier
        can_create, message = quota.can_create_challenge(is_paid)

        if not can_create:
            return Response(
                {"success": False, "error": message, "quota_exceeded": True},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate questions from curriculum
        questions = ChallengeService.generate_questions(
            language=serializer.validated_data['language'],
            category=serializer.validated_data['category'],
            difficulty=serializer.validated_data['difficulty'],
            count=serializer.validated_data['question_count']
        )

        if not questions:
            return Response(
                {"success": False, "error": "Not enough content available for this category"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create challenge
        with transaction.atomic():
            # Set expiry for free users (30 days)
            expires_at = None
            if not is_paid:
                expires_at = timezone.now() + timedelta(days=30)

            # Get child if specified
            creator_child = None
            child_id = serializer.validated_data.get('child_id')
            if child_id:
                from apps.children.models import Child
                try:
                    creator_child = Child.objects.get(id=child_id, parent=user)
                except Child.DoesNotExist:
                    pass

            challenge = Challenge.objects.create(
                creator=user,
                creator_child=creator_child,
                title=serializer.validated_data['title'],
                title_native=serializer.validated_data.get('title_native', ''),
                language=serializer.validated_data['language'],
                category=serializer.validated_data['category'],
                difficulty=serializer.validated_data['difficulty'],
                question_count=serializer.validated_data['question_count'],
                time_limit_seconds=serializer.validated_data['time_limit_seconds'],
                questions=questions,
                expires_at=expires_at,
            )

            # Record quota usage
            quota.record_challenge_created()

        response_serializer = ChallengeSerializer(challenge)
        return Response({
            "success": True,
            "data": response_serializer.data,
            "message": message
        }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def challenge_detail(request, code):
    """Get details of a specific challenge (creator only)."""
    challenge = get_object_or_404(
        Challenge,
        code=code.upper(),
        creator=request.user
    )
    serializer = ChallengeSerializer(challenge)
    return Response({
        "success": True,
        "data": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_quota(request):
    """Get user's challenge creation quota."""
    quota, _ = UserChallengeQuota.objects.get_or_create(user=request.user)
    quota.reset_if_new_day()

    serializer = QuotaSerializer(quota, context={'user': request.user})
    return Response({
        "success": True,
        "data": serializer.data
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_categories(request):
    """Get available challenge categories for a language."""
    language = request.query_params.get('language', 'HINDI')
    categories = ChallengeService.get_available_categories(language)
    serializer = CategorySerializer(categories, many=True)
    return Response({
        "success": True,
        "data": serializer.data
    })
