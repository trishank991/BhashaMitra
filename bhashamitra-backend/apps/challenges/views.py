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
import logging # Added for better debugging

from .models import Challenge, ChallengeAttempt, UserChallengeQuota
from .serializers import (
    ChallengeCreateSerializer, ChallengeSerializer, PublicChallengeSerializer,
    ChallengeAttemptCreateSerializer, ChallengeSubmitSerializer,
    ChallengeAttemptSerializer, LeaderboardEntrySerializer,
    QuotaSerializer, CategorySerializer
)
from .services import ChallengeService

logger = logging.getLogger(__name__) # Setup logging

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
    """Submit answers and get results with improved error handling."""
    # 1. Validate incoming data (Supports both snake_case and camelCase)
    serializer = ChallengeSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        logger.warning(f"Submission validation failed: {serializer.errors}")
        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Use .get() to pull data from our flexible serializer
    attempt_id = serializer.validated_data.get('attempt_id')
    answers = serializer.validated_data.get('answers')
    time_taken = serializer.validated_data.get('time_taken_seconds', 0)

    # 2. Fetch the attempt
    try:
        attempt = ChallengeAttempt.objects.select_related('challenge').get(id=attempt_id)
    except (ChallengeAttempt.DoesNotExist, ValueError):
        return Response(
            {"success": False, "error": "Attempt not found. Please refresh and try again."},
            status=status.HTTP_404_NOT_FOUND
        )

    # 3. Security: Prevent double submission
    if attempt.is_completed:
        return Response(
            {"success": False, "error": "This attempt was already submitted"},
            status=status.HTTP_400_BAD_REQUEST
        )

    challenge = attempt.challenge

    # 4. Calculate Score using Service
    try:
        result = ChallengeService.calculate_score(challenge.questions, answers)
    except Exception as e:
        logger.error(f"Score calculation error: {str(e)}")
        return Response(
            {"success": False, "error": "Error calculating results"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 5. Atomic Update to Database
    try:
        with transaction.atomic():
            attempt.score = result['score']
            attempt.max_score = result.get('max_score', challenge.question_count)
            attempt.percentage = result['percentage']
            attempt.time_taken_seconds = time_taken
            attempt.answers = result['detailed_results']
            attempt.is_completed = True
            attempt.completed_at = timezone.now()
            attempt.save()

            # Update challenge stats
            challenge.total_completions += 1
            
            # Recalculate average score safely
            completed_attempts = ChallengeAttempt.objects.filter(
                challenge=challenge,
                is_completed=True
            )
            total_percentage = sum(a.percentage for a in completed_attempts)
            
            if challenge.total_completions > 0:
                challenge.average_score = total_percentage / challenge.total_completions
            
            challenge.save(update_fields=['total_completions', 'average_score'])

    except Exception as e:
        logger.error(f"Database update failed: {str(e)}")
        return Response(
            {"success": False, "error": "Internal server error saving results"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    # 6. Return Clean Results
    return Response({
        "success": True,
        "data": {
            "score": attempt.score,
            "max_score": attempt.max_score,
            "percentage": attempt.percentage,
            "time_taken_seconds": attempt.time_taken_seconds,
            "rank": attempt.rank,
            "total_participants": challenge.total_completions,
            "detailed_results": attempt.answers,
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
    user = request.user

    if request.method == 'GET':
        challenges = Challenge.objects.filter(creator=user).order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        })

    elif request.method == 'POST':
        # --- DIAGNOSTIC LOGGING ---
        logger.info(f"Challenge POST attempt by user {user.email}")
        logger.info(f"Payload received: {request.data}")

        serializer = ChallengeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            logger.warning(f"Validation Errors: {serializer.errors}")
            return Response(
                {"success": False, "message": "Invalid data provided", "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        language = serializer.validated_data['language'].upper()
        category = serializer.validated_data['category']
        
        # Check quota
        quota, _ = UserChallengeQuota.objects.get_or_create(user=user)
        is_paid = getattr(user, 'is_premium_tier', False) or getattr(user, 'is_standard_tier', False) or user.is_staff
        can_create, message = quota.can_create_challenge(is_paid)

        if not can_create:
            return Response(
                {"success": False, "error": message, "quota_exceeded": True},
                status=status.HTTP_403_FORBIDDEN
            )

        # Generate questions
        questions = ChallengeService.generate_questions(
            language=language,
            category=category,
            difficulty=serializer.validated_data.get('difficulty', 'MEDIUM'),
            count=serializer.validated_data.get('question_count', 5)
        )

        if not questions:
            logger.error(f"Generation failed: No content for {language} - {category}")
            return Response(
                {"success": False, "error": f"Not enough content available for {language} in {category}. Need at least 4 items."},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            expires_at = None
            if not is_paid:
                expires_at = timezone.now() + timedelta(days=30)

            # Fix child_id lookup
            child_id = serializer.validated_data.get('child_id')
            creator_child = None
            if child_id:
                from apps.children.models import Child
                creator_child = Child.objects.filter(id=child_id, user=user).first()

            challenge = Challenge.objects.create(
                creator=user,
                creator_child=creator_child,
                title=serializer.validated_data['title'],
                title_native=serializer.validated_data.get('title_native', ''),
                language=language,
                category=category,
                difficulty=serializer.validated_data.get('difficulty', 'MEDIUM'),
                question_count=len(questions),
                time_limit_seconds=serializer.validated_data.get('time_limit_seconds', 60),
                questions=questions,
                expires_at=expires_at,
            )
            quota.record_challenge_created()

        return Response({
            "success": True,
            "data": ChallengeSerializer(challenge).data,
            "message": message
        }, status=status.HTTP_201_CREATED)
    
