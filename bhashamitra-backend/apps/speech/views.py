"""TTS API endpoints for BhashaMitra."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from django.http import HttpResponse
import logging

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
        "text": "नमस्ते बच्चों, आज हम एक कहानी सुनेंगे",
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

        valid_languages = ['HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'TELUGU', 'MALAYALAM', 'BENGALI', 'KANNADA', 'MARATHI']
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

            response = HttpResponse(audio_bytes, content_type='audio/wav')
            response['Content-Disposition'] = 'inline; filename="speech.wav"'
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

            response = HttpResponse(audio_bytes, content_type='audio/wav')
            response['Content-Disposition'] = f'inline; filename="page_{page_number}.wav"'
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
        "story_title": "चिड़िया और बिल्ली",
        "pages_total": 10,
        "pages_cached": 0,
        "pages_generated": 10,
        "total_cost_usd": 0.0036
    }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, story_id):
        # Check if user is admin
        if not getattr(request.user, 'role', None) == 'ADMIN':
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
