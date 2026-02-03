"""Peppi narration views for story and song reading."""
import logging
import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.stories.models import Story, StoryPage
from apps.curriculum.models import Song
from apps.speech.services.tts_service import TTSService

logger = logging.getLogger(__name__)


class PeppiNarrateStoryView(APIView):
    """
    GET /api/v1/peppi/narrate/story/{story_id}/

    Generate or retrieve cached Peppi narration for an entire story.
    Combines all page text for continuous narration.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id):
        language = request.query_params.get('language', 'HINDI')
        gender = request.query_params.get('gender', 'female')

        try:
            story = Story.objects.get(id=story_id)
        except Story.DoesNotExist:
            return Response(
                {'error': 'Story not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all pages and combine text (prefer Hindi text, fallback to text_content)
        pages = StoryPage.objects.filter(story=story).order_by('page_number')
        full_text = '\n\n'.join([
            (page.text_hindi or page.text_content) for page in pages
            if (page.text_hindi or page.text_content) and (page.text_hindi or page.text_content).strip()
        ])

        if not full_text:
            return Response(
                {'error': 'Story has no text content'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate narration using TTS with Peppi voice
        # Always use Google TTS WaveNet for Peppi narration regardless of user tier
        try:
            from unittest.mock import Mock
            peppi_user = Mock()
            peppi_user.tts_provider = 'google_wavenet'  # Force Google TTS for Peppi

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=full_text,
                language=language,
                voice_profile='kid_friendly',
                user=peppi_user,
                force_regenerate=False,
            )

            # Return audio as base64 for immediate playback (avoids file storage issues)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return Response({
                'audio_data': audio_base64,
                'audio_format': 'mp3',
                'provider': provider,
                'cached': was_cached,
                'story_title': story.title,
                'page_count': pages.count()
            })

        except Exception as e:
            logger.error(f"Peppi narration failed for story {story_id}: {e}")
            return Response(
                {'error': f'Narration generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PeppiNarrateTextView(APIView):
    """
    POST /api/v1/peppi/narrate/

    Generate Peppi narration for arbitrary text.
    Body: { "text": "...", "language": "HINDI", "gender": "female" }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text', '')
        language = request.data.get('language', 'HINDI')
        gender = request.data.get('gender', 'female')

        if not text or not text.strip():
            return Response(
                {'error': 'Text is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Always use Google TTS WaveNet for Peppi narration
            from unittest.mock import Mock
            peppi_user = Mock()
            peppi_user.tts_provider = 'google_wavenet'

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=text,
                language=language,
                voice_profile='kid_friendly',
                user=peppi_user,
                force_regenerate=False,
            )

            # Return audio as base64 for immediate playback
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return Response({
                'audio_data': audio_base64,
                'audio_format': 'mp3',
                'provider': provider,
                'cached': was_cached
            })

        except Exception as e:
            logger.error(f"Peppi narration failed: {e}")
            return Response(
                {'error': f'Narration generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PeppiNarratePageView(APIView):
    """
    GET /api/v1/peppi/narrate/story/{story_id}/page/{page_number}/

    Get narration for a single story page (for page-by-page reading).
    Returns cached audio if available, generates if not.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, story_id, page_number):
        language = request.query_params.get('language', 'HINDI')

        try:
            story = Story.objects.get(id=story_id)
            page = StoryPage.objects.get(story=story, page_number=page_number)
        except Story.DoesNotExist:
            return Response(
                {'error': 'Story not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except StoryPage.DoesNotExist:
            return Response(
                {'error': f'Page {page_number} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Use Hindi text with fallback to text_content
        page_text = page.text_hindi or page.text_content
        if not page_text or not page_text.strip():
            return Response(
                {'error': 'Page has no text content'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Always use Google TTS WaveNet for Peppi narration
            from unittest.mock import Mock
            peppi_user = Mock()
            peppi_user.tts_provider = 'google_wavenet'

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=page_text,
                language=language,
                voice_profile='kid_friendly',
                user=peppi_user,
                force_regenerate=False,
            )

            # Return audio as base64 for immediate playback
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return Response({
                'audio_data': audio_base64,
                'audio_format': 'mp3',
                'provider': provider,
                'cached': was_cached,
                'page_number': page_number,
                'text': page_text
            })

        except Exception as e:
            logger.error(f"Peppi page narration failed: {e}")
            return Response(
                {'error': f'Narration generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PeppiNarrateSongView(APIView):
    """
    GET /api/v1/peppi/narrate/song/{song_id}/

    Generate or retrieve cached Peppi narration for a song.
    Uses the Hindi lyrics for narration.

    NOTE: During testing, only one song can be cached at a time.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, song_id):
        language = request.query_params.get('language', 'HINDI')
        gender = request.query_params.get('gender', 'female')

        try:
            song = Song.objects.get(id=song_id)
        except Song.DoesNotExist:
            return Response(
                {'error': 'Song not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get lyrics text for narration
        lyrics_text = song.lyrics_hindi
        if not lyrics_text or not lyrics_text.strip():
            return Response(
                {'error': 'Song has no lyrics'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate narration using TTS with Peppi voice
        # Use 'song' voice profile for slower pace with emotions and voice modulation
        try:
            from unittest.mock import Mock
            peppi_user = Mock()
            peppi_user.tts_provider = 'google_wavenet'  # Premium quality for Peppi

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=lyrics_text,
                language=language,
                voice_profile='song',  # Song profile: slower, melodic, emotional
                user=peppi_user,
                force_regenerate=False,
            )

            # Return audio as base64 for immediate playback (avoids file storage issues)
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
            return Response({
                'audio_data': audio_base64,
                'audio_format': 'mp3',
                'provider': provider,
                'cached': was_cached,
                'song_title': song.title_english,
                'song_title_hindi': song.title_hindi
            })

        except Exception as e:
            logger.error(f"Peppi song narration failed for song {song_id}: {e}")
            return Response(
                {'error': f'Narration generation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
