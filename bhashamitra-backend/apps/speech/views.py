"""TTS API endpoints for BhashaMitra."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from django.db import models
from django.db.models import Count, Avg
from django.http import HttpResponse
import logging

from apps.speech.models import AudioCache
from apps.speech.services.tts_service import TTSService, TTSServiceError
from apps.speech.services.cache_service import AudioCacheService

logger = logging.getLogger(__name__)


class TextToSpeechView(APIView):
    """
    POST /api/v1/speech/tts/

    Generate speech from text. Returns audio file directly.

    NOTE: Public access allowed for educational content.
    Rate limiting via throttle protects against abuse.
    Authentication is optional but recommended to get tier-based TTS.

    Request Body:
    {
        "text": " ,     ",
        "language": "HINDI",
        "voice_style": "storyteller"  // optional
    }

    Response: Audio file (WAV format)

    Headers in response:
    - X-TTS-Cached: true/false
    - X-TTS-Language: HINDI
    - X-TTS-Tier: FREE/STANDARD/PREMIUM/anonymous
    - Content-Type: audio/wav
    """
    # Use default authentication (JWT) but allow unauthenticated access
    # This enables tier-based TTS routing for authenticated users
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'tts'

    def post(self, request):
        text = request.data.get('text')
        language = request.data.get('language', 'HINDI')
        voice_style = request.data.get('voice_style', 'storyteller')

        # Validation
        if not text:
            return Response(
                {"detail": "Text is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(text) > 5000:
            return Response(
                {"detail": "Text too long (max 5000 characters)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_languages = ['FIJI_HINDI', 'HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'TELUGU', 'MALAYALAM', 'BENGALI', 'KANNADA', 'MARATHI']
        if language not in valid_languages:
            return Response(
                {"detail": f"Invalid language. Must be one of: {valid_languages}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Kid-friendly voice styles for Indic Parler-TTS
        valid_styles = [
            'kid_friendly',   # Default: cheerful, high-pitched, like Miss Rachel
            'calm_story',     # Soft, gentle for bedtime stories
            'enthusiastic',   # High energy for games
            'male_teacher',   # Friendly male teacher voice
            'storyteller',    # Legacy: maps to kid_friendly
            'calm',           # Legacy: maps to calm_story
        ]
        # Map legacy styles to new ones
        style_mapping = {
            'storyteller': 'kid_friendly',
            'calm': 'calm_story',
        }
        voice_style = style_mapping.get(voice_style, voice_style)

        if voice_style not in valid_styles:
            return Response(
                {"detail": f"Invalid voice_style. Must be one of: {valid_styles}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get authenticated user for tier-based routing (or None for anonymous)
            user = request.user if request.user.is_authenticated else None
            user_tier = getattr(user, 'subscription_tier', 'anonymous') if user else 'anonymous'

            # text_to_speech returns (audio_bytes, was_cached) - legacy method
            audio_bytes, was_cached = TTSService.text_to_speech(
                text=text,
                language=language,
                voice_style=voice_style,
                user=user
            )

            # Google TTS returns MP3, so use correct content type
            response = HttpResponse(audio_bytes, content_type='audio/mpeg')
            response['Content-Disposition'] = 'inline; filename="speech.mp3"'
            response['Content-Length'] = len(audio_bytes)
            response['X-TTS-Cached'] = str(was_cached).lower()
            response['X-TTS-Language'] = language
            response['X-TTS-Tier'] = user_tier
            response['Cache-Control'] = 'public, max-age=86400'  # Browser cache 24h

            return response

        except TTSServiceError as e:
            logger.error(f"TTS error: {e}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class StoryPageAudioView(APIView):
    """
    GET /api/v1/stories/{story_id}/pages/{page_number}/audio/

    Get audio for a specific story page.
    Uses tier-based TTS provider selection:
    - FREE/STANDARD: Svara TTS
    - PREMIUM: Sarvam AI (manisha/abhilash voices)

    Query Parameters:
    - voice_style: storyteller (default), calm, enthusiastic

    Response: Audio file (WAV format)
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'tts'

    def get(self, request, story_id, page_number):
        from apps.stories.models import Story, StoryPage

        voice_style = request.query_params.get('voice_style', 'storyteller')

        # Map legacy styles
        style_mapping = {'storyteller': 'kid_friendly', 'calm': 'calm_story'}
        voice_style = style_mapping.get(voice_style, voice_style)

        try:
            story = Story.objects.get(id=story_id)
            page = StoryPage.objects.get(story=story, page_number=page_number)
        except Story.DoesNotExist:
            return Response(
                {"detail": "Story not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        except StoryPage.DoesNotExist:
            return Response(
                {"detail": f"Page {page_number} not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            # Use tier-based TTS with user context
            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=page.text_content,
                language=story.language,
                voice_profile=voice_style,
                user=request.user,  # Pass user for tier-based routing
            )

            response = HttpResponse(audio_bytes, content_type='audio/mpeg')
            response['Content-Disposition'] = f'inline; filename="page_{page_number}.mp3"'
            response['Content-Length'] = len(audio_bytes)
            response['X-TTS-Cached'] = str(was_cached).lower()
            response['X-TTS-Provider'] = provider
            response['X-Story-ID'] = str(story_id)
            response['X-Page-Number'] = str(page_number)
            response['X-Subscription-Tier'] = getattr(request.user, 'subscription_tier', 'FREE')
            response['Cache-Control'] = 'public, max-age=604800'  # Browser cache 7 days

            return response

        except TTSServiceError as e:
            logger.error(f"TTS error for story {story_id} page {page_number}: {e}")
            return Response(
                {"detail": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )


class TTSStatusView(APIView):
    """
    GET /api/v1/speech/status/

    Check TTS service health and cache statistics.

    Response:
    {
        "status": "healthy",
        "model": {"status": "ready", "model": "ai4bharat/indic-parler-tts"},
        "cache": {
            "total_entries": 150,
            "total_size_bytes": 52428800,
            "total_cost_usd": 0.054,
            "estimated_savings_usd": 1.23
        }
    }
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_info = TTSService.check_service_status()
        return Response({"data": status_info})


class PrewarmStoryAudioView(APIView):
    """
    POST /api/v1/speech/prewarm/{story_id}/

    Pre-generate and cache all audio for a story.
    Admin only - use when adding new stories.

    Response:
    {
        "story_id": "xxx",
        "story_title": "  ",
        "pages_total": 10,
        "pages_cached": 0,
        "pages_generated": 10,
        "total_cost_usd": 0.0036
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        # Check if user is admin
        if getattr(request.user, 'role', None) != 'ADMIN':
            return Response(
                {"detail": "Admin access required"},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            results = TTSService.prewarm_story(story_id)
            return Response({"data": results})

        except TTSServiceError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CurriculumAudioView(APIView):
    """
    GET /api/v1/speech/curriculum/{content_type}/{content_id}/

    Get pre-generated audio for curriculum content (alphabet, vocabulary).
    This endpoint serves cached audio for FREE tier users.

    Parameters:
    - content_type: 'alphabet' or 'vocabulary'
    - content_id: transliteration code (e.g., 'ka', 'maa')

    Query Parameters:
    - language: HINDI (default), TAMIL, etc.

    Response: Audio file (WAV format) or JSON error

    Headers:
    - X-Audio-Cached: true (always, since this serves pre-generated content)
    - Cache-Control: public, max-age=31536000 (1 year)
    """
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'tts'

    def get(self, request, content_type, content_id):
        language = request.query_params.get('language', 'HINDI')

        # Validate content type
        valid_content_types = ['alphabet', 'vocabulary', 'alphabet_letter', 'alphabet_example']
        if content_type not in valid_content_types and 'vocabulary_' not in content_type:
            return Response(
                {"detail": f"Invalid content type. Must be one of: {valid_content_types}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Look up cached audio by content type and ID
            audio_cache = AudioCache.objects.filter(
                content_type__contains=content_type,
                content_id=content_id,
                language=language,
            ).first()

            if not audio_cache:
                return Response(
                    {"detail": "Audio not found. Content may not be pre-generated yet."},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Read audio file
            if audio_cache.audio_file:
                audio_cache.audio_file.open('rb')
                audio_bytes = audio_cache.audio_file.read()
                audio_cache.audio_file.close()
            elif audio_cache.audio_url:
                # Redirect to stored URL
                return Response(
                    {"audio_url": audio_cache.audio_url},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Audio file not available"},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Update access count
            audio_cache.increment_access()

            response = HttpResponse(audio_bytes, content_type='audio/mpeg')
            response['Content-Disposition'] = f'inline; filename="{content_id}.mp3"'
            response['Content-Length'] = len(audio_bytes)
            response['X-Audio-Cached'] = 'true'
            response['X-Content-Type'] = content_type
            response['X-Content-ID'] = content_id
            response['Cache-Control'] = 'public, max-age=31536000'  # 1 year cache

            return response

        except Exception as e:
            logger.error(f"Error serving curriculum audio: {e}")
            return Response(
                {"detail": "Error retrieving audio"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CurriculumAudioListView(APIView):
    """
    GET /api/v1/speech/curriculum/

    List all available pre-generated curriculum audio.
    Useful for frontend to know what's available for offline caching.

    Query Parameters:
    - language: HINDI (default)
    - content_type: alphabet, vocabulary (optional filter)

    Response:
    {
        "language": "HINDI",
        "content": {
            "alphabet": [
                {"id": "ka", "text": "", "audio_url": "/api/v1/speech/curriculum/alphabet/ka/"},
                ...
            ],
            "vocabulary": {
                "family": [...],
                "colors": [...],
                ...
            }
        },
        "total_items": 150,
        "cache_status": "complete"
    }
    """
    permission_classes = [AllowAny]

    def get(self, request):
        language = request.query_params.get('language', 'HINDI')
        content_type_filter = request.query_params.get('content_type')

        # Get all cached curriculum content
        queryset = AudioCache.objects.filter(
            language=language,
            content_type__isnull=False,
        ).exclude(content_type='')

        if content_type_filter:
            queryset = queryset.filter(content_type__contains=content_type_filter)

        # Organize by content type
        content = {
            'alphabet': [],
            'vocabulary': {},
        }

        for item in queryset:
            entry = {
                'id': item.content_id,
                'text': item.text_content,
                'audio_url': f'/api/v1/speech/curriculum/{item.content_type}/{item.content_id}/',
            }

            if item.content_type.startswith('alphabet'):
                content['alphabet'].append(entry)
            elif item.content_type.startswith('vocabulary_'):
                category = item.content_type.replace('vocabulary_', '')
                if category not in content['vocabulary']:
                    content['vocabulary'][category] = []
                content['vocabulary'][category].append(entry)

        total_items = queryset.count()

        return Response({
            'language': language,
            'content': content,
            'total_items': total_items,
            'cache_status': 'complete' if total_items > 0 else 'empty',
        })


# ========================================
# PEPPI MIMIC VIEWS
# ========================================

from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Avg, Sum, Count, Max
from apps.speech.models import PeppiMimicChallenge, PeppiMimicAttempt, PeppiMimicProgress
from apps.speech.serializers import (
    MimicChallengeListSerializer,
    MimicChallengeDetailSerializer,
    MimicAttemptSerializer,
    MimicAttemptSubmitSerializer,
    MimicAttemptResultSerializer,
    MimicProgressSerializer,
    MimicProgressSummarySerializer,
    MimicShareSerializer,
)
from apps.speech.services.pronunciation_scorer import pronunciation_scorer
from apps.speech.services.stt_service import stt_service
from apps.children.models import Child


class MimicChallengeListView(APIView):
    """
    GET /api/v1/speech/mimic/challenges/

    List pronunciation challenges for a child.

    Query Parameters:
    - child_id: UUID of the child (required)
    - category: GREETING, FAMILY, NUMBERS, COLORS, FESTIVAL, etc.
    - difficulty: 1, 2, or 3
    - limit: max results (default 20)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        child_id = request.query_params.get('child_id')
        if not child_id:
            return Response(
                {"detail": "child_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        child = get_object_or_404(Child, id=child_id, user=request.user)

        # Build queryset
        queryset = PeppiMimicChallenge.objects.filter(
            is_active=True,
            language=child.language
        )

        # Filter by category
        category = request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category.upper())

        # Filter by difficulty
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            queryset = queryset.filter(difficulty=int(difficulty))

        # Limit results
        limit = int(request.query_params.get('limit', 20))
        queryset = queryset[:limit]

        # Get child's progress for these challenges
        challenge_ids = [str(c.id) for c in queryset]
        progress_qs = PeppiMimicProgress.objects.filter(
            child=child,
            challenge_id__in=challenge_ids
        )
        progress_map = {str(p.challenge_id): p for p in progress_qs}

        # Serialize
        serializer = MimicChallengeListSerializer(
            queryset,
            many=True,
            context={'progress_map': progress_map}
        )

        return Response({
            'results': serializer.data,
            'categories': dict(PeppiMimicChallenge.Category.choices),
            'total': len(serializer.data),
        })


class MimicChallengeDetailView(APIView):
    """
    GET /api/v1/speech/mimic/challenges/{challenge_id}/

    Get detailed info for a specific challenge.

    Query Parameters:
    - child_id: UUID of the child (required)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, challenge_id):
        # Get child_id from query params
        child_id = request.query_params.get('child_id')
        if not child_id:
            return Response(
                {"detail": "child_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        child = get_object_or_404(Child, id=child_id, user=request.user)
        challenge = get_object_or_404(
            PeppiMimicChallenge,
            id=challenge_id,
            is_active=True
        )

        serializer = MimicChallengeDetailSerializer(
            challenge,
            context={'child': child}
        )

        return Response(serializer.data)


class MimicAttemptThrottle(ScopedRateThrottle):
    """Rate limit pronunciation attempts to prevent spam."""
    scope = 'mimic_attempts'
    THROTTLE_RATES = {'mimic_attempts': '30/minute'}


class MimicAttemptSubmitView(APIView):
    """
    POST /api/v1/speech/mimic/challenges/{challenge_id}/attempt/

    Submit a pronunciation attempt for scoring.

    Request Body:
    {
        "audio_url": "https://r2.example.com/recordings/xxx.webm",
        "duration_ms": 3000,
        "child_id": "uuid"  // Required
    }

    Response:
    {
        "attempt_id": "uuid",
        "transcription": "",
        "score": 85.5,
        "stars": 3,
        "points_earned": 35,
        "is_personal_best": true,
        "mastered": true,
        "peppi_feedback": "WOOOW! Perfect!",
        "share_message": "...",
        "progress": {...},
        "score_breakdown": {...}  // V2: Detailed scoring breakdown
    }
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [MimicAttemptThrottle]

    def post(self, request, challenge_id):
        # Get child_id from request body
        child_id = request.data.get('child_id')
        if not child_id:
            return Response(
                {"detail": "child_id is required in request body"},
                status=status.HTTP_400_BAD_REQUEST
            )

        child = get_object_or_404(Child, id=child_id, user=request.user)
        challenge = get_object_or_404(
            PeppiMimicChallenge,
            id=challenge_id,
            is_active=True
        )

        # Validate input
        serializer = MimicAttemptSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        audio_url = serializer.validated_data['audio_url']
        duration_ms = serializer.validated_data.get('duration_ms', 3000)

        try:
            # Step 1: Transcribe audio using STT
            stt_result = stt_service.transcribe(
                audio_url=audio_url,
                language=challenge.language,
                expected_word=challenge.word  # For mock STT testing
            )

            # Step 2: Get expected duration from reference audio (if available)
            expected_duration_ms = None
            if challenge.audio_cache and challenge.audio_cache.audio_duration_ms:
                expected_duration_ms = challenge.audio_cache.audio_duration_ms

            # Step 3: Score the pronunciation with V2 acoustic analysis
            score_result = pronunciation_scorer.score(
                transcription=stt_result.transcription,
                expected_word=challenge.word,
                stt_confidence=stt_result.confidence,
                language_name=challenge.language,  # <--- ADDED THIS
                expected_romanization=challenge.romanization,
                audio_url=audio_url, 
                expected_duration_ms=expected_duration_ms 
            )

            # Step 4: Get or create progress record
            progress, created = PeppiMimicProgress.objects.get_or_create(
                child=child,
                challenge=challenge
            )

            # Step 5: Check if personal best
            is_personal_best = score_result.final_score > progress.best_score

            # Step 6: Calculate points
            points = pronunciation_scorer.get_points(
                score_result.stars,
                is_personal_best
            )

            # Step 6.5: Truncate transcription to fit database field (max 200 chars)
            transcription = stt_result.transcription or ''
            MAX_TRANSCRIPTION_LENGTH = 200
            if len(transcription) > MAX_TRANSCRIPTION_LENGTH:
                logger.warning(
                    f"Truncating transcription from {len(transcription)} to {MAX_TRANSCRIPTION_LENGTH} chars"
                )
                transcription = transcription[:MAX_TRANSCRIPTION_LENGTH - 3] + '...'

            # Step 7: Create attempt record with V2 acoustic fields
            attempt = PeppiMimicAttempt.objects.create(
                child=child,
                challenge=challenge,
                audio_url=audio_url,
                duration_ms=duration_ms,
                stt_transcription=transcription,
                stt_confidence=stt_result.confidence,
                text_match_score=score_result.text_match_score,
                final_score=score_result.final_score,
                stars=score_result.stars,
                # V2 acoustic analysis fields
                audio_energy_score=score_result.energy_score,
                duration_match_score=score_result.duration_match_score,
                scoring_version=score_result.scoring_version,
                # Points and status
                points_earned=points,
                is_personal_best=is_personal_best
            )

            # Step 8: Update progress
            progress.update_from_attempt(attempt)

            # Step 9: Update child's total points
            child.total_points += points
            child.save(update_fields=['total_points'])

            # Step 10: Get Peppi feedback
            peppi_feedback = pronunciation_scorer.get_peppi_feedback(
                challenge,
                score_result.feedback_key,
                child.name
            )

            # Step 11: Generate share message
            share_message = pronunciation_scorer.generate_share_message(
                child_name=child.name,
                word=challenge.word,
                romanization=challenge.romanization,
                language=challenge.language,
                stars=score_result.stars,
                score=score_result.final_score
            )

            return Response({
                'attempt_id': attempt.id,
                'transcription': stt_result.transcription,
                'score': score_result.final_score,
                'stars': score_result.stars,
                'coach_tip': score_result.ai_coach_tip,
                'points_earned': points,
                'is_personal_best': is_personal_best,
                'mastered': progress.mastered,
                'peppi_feedback': peppi_feedback,
                'share_message': share_message,
                'progress': {
                    'best_score': progress.best_score,
                    'best_stars': progress.best_stars,
                    'total_attempts': progress.total_attempts,
                    'mastered': progress.mastered,
                },
                # V2: Include detailed score breakdown
                'score_breakdown': score_result.score_breakdown,
                'scoring_version': score_result.scoring_version,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing mimic attempt: {e}")
            return Response(
                {'detail': f'Error processing attempt: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MimicProgressView(APIView):
    """
    GET /api/v1/speech/mimic/progress/

    Get child's overall mimic progress summary.

    Query Parameters:
    - child_id: UUID of the child (required)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        child_id = request.query_params.get('child_id')
        if not child_id:
            return Response(
                {"detail": "child_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        child = get_object_or_404(Child, id=child_id, user=request.user)

        # Get all progress records
        progress_qs = PeppiMimicProgress.objects.filter(child=child)

        # Calculate stats
        total_challenges = PeppiMimicChallenge.objects.filter(
            is_active=True,
            language=child.language
        ).count()

        stats = progress_qs.aggregate(
            total_attempts=Sum('total_attempts'),
            total_points=Sum('total_points'),
            avg_score=Avg('best_score'),
            current_streak=Max('current_streak'),
            longest_streak=Max('longest_streak'),
        )

        challenges_attempted = progress_qs.count()
        challenges_mastered = progress_qs.filter(mastered=True).count()

        # Get category breakdown
        categories = progress_qs.values('challenge__category').annotate(
            count=Count('id'),
            mastered=Count('id', filter=models.Q(mastered=True)),
            avg_score=Avg('best_score')
        )

        return Response({
            'total_challenges': total_challenges,
            'challenges_attempted': challenges_attempted,
            'challenges_mastered': challenges_mastered,
            'total_attempts': stats['total_attempts'] or 0,
            'total_points': stats['total_points'] or 0,
            'average_score': round(stats['avg_score'] or 0, 1),
            'current_streak': stats['current_streak'] or 0,
            'longest_streak': stats['longest_streak'] or 0,
            'categories': list(categories),
        })


class MimicAttemptShareView(APIView):
    """
    PATCH /api/v1/speech/mimic/attempts/{attempt_id}/share/

    Mark an attempt as shared to family.

    Request Body:
    {
        "child_id": "uuid",  // Required
        "shared_to_family": true
    }
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request, attempt_id):
        # Get child_id from request body
        child_id = request.data.get('child_id')
        if not child_id:
            return Response(
                {"detail": "child_id is required in request body"},
                status=status.HTTP_400_BAD_REQUEST
            )

        child = get_object_or_404(Child, id=child_id, user=request.user)
        attempt = get_object_or_404(
            PeppiMimicAttempt,
            id=attempt_id,
            child=child
        )

        serializer = MimicShareSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if serializer.validated_data['shared_to_family']:
            attempt.shared_to_family = True
            attempt.shared_at = timezone.now()
            attempt.save(update_fields=['shared_to_family', 'shared_at'])

        return Response({
            'id': attempt.id,
            'shared_to_family': attempt.shared_to_family,
            'shared_at': attempt.shared_at,
        })


class AudioUploadView(APIView):
    """
    POST /api/v1/speech/upload-audio/

    Upload audio recording for mimic attempts.
    Stores audio and returns URL for STT processing.

    Request: multipart/form-data
    - audio: Audio file (webm, wav, mp3)
    - child_id: Child UUID (for organizing files)

    Response:
    {
        "audio_url": "https://storage.example.com/mimic-recordings/xxx.webm"
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from django.core.files.storage import default_storage
        from django.core.files.base import ContentFile
        import uuid
        import os

        audio_file = request.FILES.get('audio')
        child_id = request.data.get('child_id')

        if not audio_file:
            return Response(
                {'detail': 'Audio file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate file type
        allowed_types = ['audio/webm', 'audio/wav', 'audio/mpeg', 'audio/mp3', 'audio/ogg']
        content_type = audio_file.content_type

        # Some browsers send different content types
        if content_type not in allowed_types and not content_type.startswith('audio/'):
            return Response(
                {'detail': f'Invalid audio format. Allowed: {allowed_types}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate file size (max 10MB)
        if audio_file.size > 10 * 1024 * 1024:
            return Response(
                {'detail': 'Audio file too large (max 10MB)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Generate unique filename
            ext = os.path.splitext(audio_file.name)[1] or '.webm'
            unique_id = uuid.uuid4().hex[:12]
            filename = f"mimic_recordings/{child_id or 'anon'}/{unique_id}{ext}"

            # Save file
            saved_path = default_storage.save(filename, ContentFile(audio_file.read()))

            # Get the URL
            if hasattr(default_storage, 'url'):
                audio_url = default_storage.url(saved_path)
            else:
                # Fallback for local storage
                audio_url = f"/media/{saved_path}"

            # Make URL absolute if needed
            if audio_url.startswith('/'):
                from django.conf import settings
                base_url = getattr(settings, 'SITE_URL', '') or request.build_absolute_uri('/').rstrip('/')
                audio_url = f"{base_url.rstrip('/')}{audio_url}"

            logger.info(f"Audio uploaded: {saved_path}, url: {audio_url}")

            return Response({
                'audio_url': audio_url,
                'filename': saved_path,
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error uploading audio: {e}")
            return Response(
                {'detail': f'Error uploading audio: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SpeechToTextView(APIView):
    """
    POST /api/v1/speech/stt/

    Transcribe speech to text using Google Cloud STT.
    Optionally evaluates pronunciation against expected text.

    Request Body:
    {
        "audio_url": "https://example.com/audio.webm",
        "language": "HINDI",
        "expected_text": "namaste",  // Optional - for pronunciation scoring
        "attempt_number": 1  // Optional - for varied feedback messages
    }

    Response (with expected_text):
    {
        "success": true,
        "data": {
            "transcription": "namaste",
            "confidence": 92,
            "evaluation": {
                "score": 95,
                "stars": 3,
                "is_correct": true,
                "expected": {"native": "namaste", "roman": "namaste"},
                "heard": {"native": "namaste", "roman": "namaste"},
                "feedback": {
                    "level": "excellent",
                    "emoji": "star",
                    "message_hindi": "bahut badhiya!",
                    "message_english": "Amazing pronunciation!",
                    "encouragement": "You sound just like a native speaker!"
                },
                "word_comparison": [...],
                "hints": []
            }
        }
    }
    """
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'speech'

    def post(self, request):
        from apps.speech.services.stt_service import stt_service
        from apps.speech.services.transliteration import evaluate_pronunciation_enhanced

        audio_url = request.data.get('audio_url')
        language = request.data.get('language', 'HINDI')
        expected_text = request.data.get('expected_text')  # For pronunciation evaluation
        attempt_number = request.data.get('attempt_number', 1)

        # Validation
        if not audio_url:
            return Response(
                {'detail': 'audio_url is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_languages = ['FIJI_HINDI', 'HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'TELUGU', 'MALAYALAM', 'BENGALI', 'KANNADA', 'MARATHI', 'ODIA']
        if language not in valid_languages:
            return Response(
                {'detail': f'Invalid language. Must be one of: {valid_languages}'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Transcribe audio using STT service
            stt_result = stt_service.transcribe(
                audio_url=audio_url,
                language=language,
                expected_word=expected_text  # For mock testing
            )

            response_data = {
                'success': True,
                'data': {
                    'transcription': stt_result.transcription,
                    'confidence': int(stt_result.confidence * 100),
                    'provider': stt_result.provider,
                    'duration_ms': stt_result.duration_ms,
                }
            }

            # If expected text provided, evaluate pronunciation with enhanced feedback
            if expected_text:
                evaluation = evaluate_pronunciation_enhanced(
                    expected_text=expected_text,
                    transcribed_text=stt_result.transcription,
                    confidence=stt_result.confidence,
                    language=language,
                    attempt_number=attempt_number,
                )
                response_data['data']['evaluation'] = evaluation

            return Response(response_data)

        except Exception as e:
            logger.exception(f'STT service error: {e}')
            return Response({
                'success': False,
                'error': str(e),
                'data': {
                    'transcription': '',
                    'confidence': 0,
                }
            }, status=status.HTTP_200_OK)  # Return 200 with error in body for graceful handling