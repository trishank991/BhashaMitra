"""
Challenge API Views.

Public endpoints (AllowAny):
- GET  /api/v1/challenges/play/<code>/     - Get challenge to play
- POST /api/v1/challenges/play/<code>/     - Start attempt
- POST /api/v1/challenges/submit/           - Submit answers
- GET  /api/v1/challenges/leaderboard/<code>/ - Get leaderboard

Authenticated endpoints (Creator only):
- GET  /api/v1/challenges/                 - List my challenges
- POST /api/v1/challenges/                 - Create challenge
- GET  /api/v1/challenges/<code>/          - Get detail
- GET  /api/v1/challenges/quota/           - Get quota
- GET  /api/v1/challenges/categories/      - Get categories
"""

import logging
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Challenge, ChallengeAttempt, UserChallengeQuota
from .serializers import (
    ChallengeCreateSerializer, ChallengeSerializer, PublicChallengeSerializer,
    ChallengeAttemptCreateSerializer, ChallengeSubmitSerializer,
    ChallengeAttemptSerializer, LeaderboardEntrySerializer,
    QuotaSerializer, CategorySerializer
)
from .services import ChallengeService

logger = logging.getLogger(__name__)

# =============================================================================
# PUBLIC ENDPOINTS - No authentication required
# =============================================================================

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def play_challenge(request, code):
    """GET info or POST to start a new attempt."""
    challenge = get_object_or_404(Challenge, code=code.upper(), is_active=True)

    if challenge.is_expired:
        return Response(
            {"error": "This challenge has expired", "expired": True},
            status=status.HTTP_410_GONE
        )

    if request.method == 'GET':
        serializer = PublicChallengeSerializer(challenge)
        return Response({"success": True, "data": serializer.data})

    elif request.method == 'POST':
        serializer = ChallengeAttemptCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=400)

        attempt = ChallengeAttempt.objects.create(
            challenge=challenge,
            participant_name=serializer.validated_data['participant_name'],
            participant_location=serializer.validated_data.get('participant_location', ''),
            max_score=challenge.question_count,
            participant_user=request.user if request.user.is_authenticated else None,
        )

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
    """Submit answers and calculate results."""
    serializer = ChallengeSubmitSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"success": False, "errors": serializer.errors}, status=400)

    attempt_id = serializer.validated_data.get('attempt_id')
    answers = serializer.validated_data.get('answers')
    time_taken = serializer.validated_data.get('time_taken_seconds', 0)

    try:
        attempt = ChallengeAttempt.objects.select_related('challenge').get(id=attempt_id)
    except (ChallengeAttempt.DoesNotExist, ValueError):
        return Response({"success": False, "error": "Attempt not found."}, status=404)

    if attempt.is_completed:
        return Response({"success": False, "error": "Already submitted"}, status=400)

    challenge = attempt.challenge
    result = ChallengeService.calculate_score(challenge.questions, answers)

    with transaction.atomic():
        attempt.score = result['score']
        attempt.max_score = result.get('max_score', challenge.question_count)
        attempt.percentage = result['percentage']
        attempt.time_taken_seconds = time_taken
        attempt.answers = result['detailed_results']
        attempt.is_completed = True
        attempt.completed_at = timezone.now()
        attempt.save()

        challenge.total_completions += 1
        completed_attempts = ChallengeAttempt.objects.filter(challenge=challenge, is_completed=True)
        total_percentage = sum(a.percentage for a in completed_attempts)
        challenge.average_score = total_percentage / challenge.total_completions
        challenge.save(update_fields=['total_completions', 'average_score'])

    return Response({
        "success": True,
        "data": {
            "score": attempt.score,
            "max_score": attempt.max_score,
            "percentage": attempt.percentage,
            "rank": attempt.rank,
            "detailed_results": attempt.answers,
            "share_url": challenge.share_url
        }
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def challenge_leaderboard(request, code):
    challenge = get_object_or_404(Challenge, code=code.upper())
    attempts = ChallengeAttempt.objects.filter(
        challenge=challenge, is_completed=True
    ).order_by('-percentage', 'time_taken_seconds')[:20]
    
    return Response({
        "success": True,
        "data": {
            "challenge_title": challenge.title,
            "leaderboard": LeaderboardEntrySerializer(attempts, many=True).data
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
        return Response({"success": True, "data": ChallengeSerializer(challenges, many=True).data})

    elif request.method == 'POST':
        logger.info(f"Payload received: {request.data}")
        serializer = ChallengeCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=400)

        language = serializer.validated_data['language'].upper()
        category = serializer.validated_data['category']
        
        quota, _ = UserChallengeQuota.objects.get_or_create(user=user)
        is_paid = getattr(user, 'is_premium_tier', False) or getattr(user, 'is_standard_tier', False) or user.is_staff
        can_create, message = quota.can_create_challenge(is_paid)

        if not can_create:
            return Response({"success": False, "error": message}, status=403)

        # FIXED METHOD NAME
        questions = ChallengeService.get_random_questions(
            language=language,
            category=category,
            difficulty=serializer.validated_data.get('difficulty', 'easy'),
            count=serializer.validated_data.get('question_count', 5)
        )

        if not questions:
            return Response({"success": False, "error": f"No content for {language} {category}."}, status=400)

        with transaction.atomic():
            expires_at = None if is_paid else timezone.now() + timedelta(days=30)
            
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
                difficulty=serializer.validated_data.get('difficulty', 'easy'),
                question_count=len(questions),
                time_limit_seconds=serializer.validated_data.get('time_limit_seconds', 30),
                questions=questions,
                expires_at=expires_at,
            )
            quota.record_challenge_created()

        return Response({"success": True, "data": ChallengeSerializer(challenge).data}, status=201)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def challenge_detail(request, code):
    challenge = get_object_or_404(Challenge, code=code.upper(), creator=request.user)
    return Response({"success": True, "data": ChallengeSerializer(challenge).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_quota(request):
    quota, _ = UserChallengeQuota.objects.get_or_create(user=request.user)
    quota.reset_if_new_day()
    return Response({"success": True, "data": QuotaSerializer(quota, context={'user': request.user}).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_categories(request):
    language = request.query_params.get('language', 'HINDI').upper()
    categories = ChallengeService.get_available_categories(language)
    return Response({"success": True, "data": CategorySerializer(categories, many=True).data})
