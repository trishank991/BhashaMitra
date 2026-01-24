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
# DEPLOY_VER: 2026-01-03-V4-FINAL
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db import transaction
from datetime import timedelta

from .models import Challenge, UserChallengeQuota
from .serializers import ChallengeCreateSerializer, ChallengeSerializer, CategorySerializer, QuotaSerializer
from .services.challenge_service import ChallengeService

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def challenges_list_create(request):
    if request.method == 'GET':
        challenges = Challenge.objects.filter(creator=request.user).order_by('-created_at')
        return Response({"success": True, "data": ChallengeSerializer(challenges, many=True).data})

    serializer = ChallengeCreateSerializer(data=request.data)
    if serializer.is_valid():
        language = serializer.validated_data['language'].upper()
        questions = ChallengeService.get_random_questions(
            language=language,
            category=serializer.validated_data['category'],
            count=serializer.validated_data.get('question_count', 5)
        )
        if not questions:
            return Response({"success": False, "error": "Not enough content."}, status=400)

        challenge = Challenge.objects.create(
            creator=request.user,
            title=serializer.validated_data['title'],
            language=language,
            category=serializer.validated_data['category'],
            questions=questions
        )
        return Response({"success": True, "data": ChallengeSerializer(challenge).data}, status=201)
    
    # Format errors properly
    error_message = "; ".join(f"{field}: {', '.join(errors)}" for field, errors in serializer.errors.items())
    return Response({"success": False, "error": error_message or "Validation failed"}, status=400)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def play_challenge(request, code):
    from .models import ChallengeAttempt

    challenge = get_object_or_404(Challenge, code=code)

    # Helper to build full challenge response (matches PublicChallengeResponse)
    def build_challenge_data(include_questions=True):
        data = {
            "id": str(challenge.id),
            "code": challenge.code,
            "title": challenge.title,
            "title_native": challenge.title_native or "",
            "language": challenge.language,
            "language_name": challenge.get_language_display(),  # Django's built-in for choices
            "category": challenge.category,
            "difficulty": challenge.difficulty,
            "question_count": len(challenge.questions) if challenge.questions else 0,
            "time_limit_seconds": challenge.time_limit_seconds,
            "is_expired": challenge.is_expired,
            "creator_name": challenge.creator.email.split('@')[0] if challenge.creator else "Anonymous",
        }
        if include_questions:
            data["questions"] = ChallengeService.strip_answers(challenge.questions)
        return data

    if request.method == 'POST':
        # POST: Start a challenge attempt
        participant_name = request.data.get('participant_name', 'Anonymous')
        participant_location = request.data.get('participant_location', '')

        # Create the attempt record (not yet completed)
        attempt = ChallengeAttempt.objects.create(
            challenge=challenge,
            participant_name=participant_name[:50],  # Limit length
            participant_location=participant_location[:50] if participant_location else '',
            participant_user=request.user if request.user.is_authenticated else None,
            is_completed=False,
        )

        return Response({
            "success": True,
            "data": {
                "attempt_id": str(attempt.id),
                "challenge": build_challenge_data(include_questions=True),
                "started_at": timezone.now().isoformat()
            }
        })

    # GET: Return full challenge info for display
    return Response({
        "success": True,
        "data": build_challenge_data(include_questions=True)
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_challenge(request):
    """
    Submit answers for a challenge and persist the attempt.

    Request Body (with attempt_id from play_challenge POST):
    {
        "attempt_id": "uuid-here",
        "answers": [0, 2, 1, 3, 0],
        "time_taken_seconds": 120
    }

    OR legacy format (without attempt_id):
    {
        "code": "7K3M",
        "answers": [0, 2, 1, 3, 0],
        "participant_name": "Aarav",
        "participant_location": "Auckland",
        "time_taken": 120
    }
    """
    from .models import ChallengeAttempt
    from django.db.models import Avg

    attempt_id = request.data.get('attempt_id')
    answers = request.data.get('answers', [])
    time_taken = request.data.get('time_taken_seconds') or request.data.get('time_taken', 0)

    if attempt_id:
        # New flow: Update existing attempt created by play_challenge POST
        attempt = get_object_or_404(ChallengeAttempt, id=attempt_id)
        challenge = attempt.challenge
    else:
        # Legacy flow: Create new attempt using code
        code = request.data.get('code')
        if not code:
            return Response(
                {"success": False, "error": "Either attempt_id or code is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        challenge = get_object_or_404(Challenge, code=code)
        participant_name = request.data.get('participant_name', 'Anonymous')
        participant_location = request.data.get('participant_location', '')
        attempt = ChallengeAttempt.objects.create(
            challenge=challenge,
            participant_name=participant_name[:50],
            participant_location=participant_location[:50] if participant_location else '',
            participant_user=request.user if request.user.is_authenticated else None,
            is_completed=False,
        )

    # Log for debugging scoring issues
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"Scoring challenge {challenge.code}: {len(challenge.questions)} questions, {len(answers)} answers")
    if challenge.questions:
        first_q = challenge.questions[0]
        logger.info(f"First question has correct_index: {'correct_index' in first_q}, keys: {list(first_q.keys())}")

    # Calculate score
    result = ChallengeService.calculate_score(challenge.questions, answers)

    # Update the attempt with results
    attempt.score = result['score']
    attempt.max_score = result['max_score']
    attempt.percentage = result['percentage']
    attempt.time_taken_seconds = time_taken
    attempt.answers = answers
    attempt.is_completed = True
    attempt.completed_at = timezone.now()
    attempt.save()

    # Update challenge stats
    challenge.total_attempts += 1
    challenge.total_completions += 1
    # Recalculate average score
    all_attempts = ChallengeAttempt.objects.filter(challenge=challenge, is_completed=True)
    if all_attempts.exists():
        avg = all_attempts.aggregate(avg=Avg('percentage'))['avg']
        challenge.average_score = avg or 0
    challenge.save(update_fields=['total_attempts', 'total_completions', 'average_score'])

    # Build response with additional info (matching ChallengeResultResponse)
    result['attempt_id'] = str(attempt.id)
    result['rank'] = attempt.rank
    result['participant_name'] = attempt.participant_name
    result['challenge_title'] = challenge.title
    result['share_url'] = f"/c/{challenge.code}"
    result['total_participants'] = all_attempts.count()
    result['time_taken_seconds'] = time_taken

    return Response({"success": True, "data": result})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_languages(request):
    return Response({"success": True, "data": ChallengeService.get_available_languages()})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_categories(request):
    lang = request.query_params.get('language', 'HINDI')
    return Response({"success": True, "data": ChallengeService.get_available_categories(lang)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_quota(request):
    quota, _ = UserChallengeQuota.objects.get_or_create(user=request.user)
    return Response({"success": True, "data": QuotaSerializer(quota).data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def challenge_detail(request, code):
    challenge = get_object_or_404(Challenge, code=code, creator=request.user)
    return Response({"success": True, "data": ChallengeSerializer(challenge).data})

@api_view(['GET'])
@permission_classes([AllowAny])
def challenge_leaderboard(request, code):
    """
    Get leaderboard for a challenge.

    Query Parameters:
    - limit: Max results (default 50)

    Response:
    [
        {
            "rank": 1,
            "participant_name": "Aarav",
            "participant_location": "Auckland",
            "score": 5,
            "max_score": 5,
            "percentage": 100.0,
            "time_taken_seconds": 45,
            "completed_at": "2025-01-19T12:00:00Z"
        },
        ...
    ]
    """
    from .models import ChallengeAttempt

    challenge = get_object_or_404(Challenge, code=code)
    limit = int(request.query_params.get('limit', 50))

    # Get top attempts ordered by percentage (desc), then time (asc)
    attempts = ChallengeAttempt.objects.filter(
        challenge=challenge,
        is_completed=True
    ).order_by('-percentage', 'time_taken_seconds')[:limit]

    leaderboard = []
    for i, attempt in enumerate(attempts, 1):
        leaderboard.append({
            'rank': i,
            'participant_name': attempt.participant_name,
            'participant_location': attempt.participant_location,
            'score': attempt.score,
            'max_score': attempt.max_score,
            'percentage': attempt.percentage,
            'time_taken_seconds': attempt.time_taken_seconds,
            'completed_at': attempt.completed_at.isoformat() if attempt.completed_at else None,
        })

    return Response({
        "success": True,
        "data": leaderboard,
        "challenge": {
            "code": challenge.code,
            "title": challenge.title,
            "total_participants": challenge.attempts.filter(is_completed=True).count(),
            "average_score": round(challenge.average_score, 1),
        }
    })