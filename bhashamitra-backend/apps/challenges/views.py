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
    challenge = get_object_or_404(Challenge, code=code)
    
    if request.method == 'POST':
        # POST: Start a challenge attempt or just return success for starting
        return Response({
            "success": True,
            "data": {
                "message": "Challenge ready to play",
                "code": challenge.code,
                "title": challenge.title,
                "questions": ChallengeService.strip_answers(challenge.questions),
                "started_at": timezone.now().isoformat()
            }
        })
    
    # GET: Return challenge info
    return Response({
        "success": True, 
        "data": {
            "title": challenge.title,
            "questions": ChallengeService.strip_answers(challenge.questions)
        }
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_challenge(request):
    code = request.data.get('code')
    answers = request.data.get('answers', [])
    challenge = get_object_or_404(Challenge, code=code)
    result = ChallengeService.calculate_score(challenge.questions, answers)
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
    return Response({"success": True, "data": []})