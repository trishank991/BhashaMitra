"""
Google Cloud TTS Provider (Fallback)
Reliable commercial TTS for Indian languages

Cost: ~$4 per 1 million characters (Standard voices)
      ~$16 per 1 million characters (Neural voices)
"""
import os
import logging
import time
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class GoogleTTSError(Exception):
    """Google TTS specific error."""
    pass


class GoogleTTSProvider:
    """
    Google Cloud Text-to-Speech Provider

    Supported Indian languages:
    - Hindi (hi-IN)
    - Tamil (ta-IN)
    - Telugu (te-IN)
    - Gujarati (gu-IN)
    - Malayalam (ml-IN)
    - Bengali (bn-IN)
    - Kannada (kn-IN)
    - Marathi (mr-IN)

    Note: Punjabi (pa-IN) may have limited support
    """

    # Language to Google voice mapping
    VOICE_MAPPING = {
        'HINDI': {
            'language_code': 'hi-IN',
            'voice_name': 'hi-IN-Standard-A',  # Female
            'voice_name_male': 'hi-IN-Standard-B',
            'neural_voice': 'hi-IN-Neural2-A',
        },
        'TAMIL': {
            'language_code': 'ta-IN',
            'voice_name': 'ta-IN-Standard-A',
            'voice_name_male': 'ta-IN-Standard-B',
            'neural_voice': 'ta-IN-Neural2-A',
        },
        'TELUGU': {
            'language_code': 'te-IN',
            'voice_name': 'te-IN-Standard-A',
            'voice_name_male': 'te-IN-Standard-B',
            'neural_voice': 'te-IN-Neural2-A',
        },
        'GUJARATI': {
            'language_code': 'gu-IN',
            'voice_name': 'gu-IN-Standard-A',
            'voice_name_male': 'gu-IN-Standard-B',
            'neural_voice': 'gu-IN-Neural2-A',
        },
        'MALAYALAM': {
            'language_code': 'ml-IN',
            'voice_name': 'ml-IN-Standard-A',
            'voice_name_male': 'ml-IN-Standard-B',
            'neural_voice': 'ml-IN-Neural2-A',
        },
        'BENGALI': {
            'language_code': 'bn-IN',
            'voice_name': 'bn-IN-Standard-A',
            'voice_name_male': 'bn-IN-Standard-B',
            'neural_voice': 'bn-IN-Neural2-A',
        },
        'KANNADA': {
            'language_code': 'kn-IN',
            'voice_name': 'kn-IN-Standard-A',
            'voice_name_male': 'kn-IN-Standard-B',
            'neural_voice': 'kn-IN-Neural2-A',
        },
        'MARATHI': {
            'language_code': 'mr-IN',
            'voice_name': 'mr-IN-Standard-A',
            'voice_name_male': 'mr-IN-Standard-B',
            'neural_voice': 'mr-IN-Neural2-A',
        },
        'PUNJABI': {
            'language_code': 'pa-IN',
            'voice_name': 'pa-IN-Standard-A',
            'voice_name_male': 'pa-IN-Standard-B',
            'neural_voice': None,  # May not exist
        },
    }

    # Cost per character in USD
    COST_PER_CHAR_STANDARD = 4.0 / 1_000_000  # $4 per million
    COST_PER_CHAR_NEURAL = 16.0 / 1_000_000   # $16 per million

    @classmethod
    def is_available(cls) -> bool:
        """Check if Google Cloud TTS is configured."""
        # Check for credentials file
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            return True

        # Check for default credentials (GCE, Cloud Run, etc.)
        try:
            from google.auth import default
            credentials, project = default()
            return credentials is not None
        except Exception:
            return False

    @classmethod
    def generate(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_profile: str = 'default',
        use_neural: bool = False,
    ) -> Tuple[bytes, int]:
        """
        Generate TTS audio using Google Cloud.

        Args:
            text: Text to convert to speech
            language: Language code (HINDI, TAMIL, etc.)
            voice_profile: Voice style (maps to gender: 'male' or 'female')
            use_neural: Use neural voices (higher quality, more expensive)

        Returns:
            Tuple of (audio_bytes, duration_ms)

        Raises:
            GoogleTTSError: If generation fails
        """
        try:
            from google.cloud import texttospeech
        except ImportError:
            raise GoogleTTSError(
                "google-cloud-texttospeech not installed. "
                "Run: pip install google-cloud-texttospeech"
            )

        voice_config = cls.VOICE_MAPPING.get(language, cls.VOICE_MAPPING['HINDI'])
        start_time = time.time()

        try:
            logger.info(f"Google TTS: Generating audio for '{text[:50]}...' in {language}")

            client = texttospeech.TextToSpeechClient()

            synthesis_input = texttospeech.SynthesisInput(text=text)

            # Select voice based on profile
            if voice_profile == 'male':
                voice_name = voice_config.get('voice_name_male', voice_config['voice_name'])
            elif use_neural and voice_config.get('neural_voice'):
                voice_name = voice_config['neural_voice']
            else:
                voice_name = voice_config['voice_name']

            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config['language_code'],
                name=voice_name,
            )

            # Audio configuration optimized for children's learning
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.LINEAR16,
                speaking_rate=0.9,  # Slightly slower for learning
                pitch=0.0,  # Normal pitch
                sample_rate_hertz=22050,
                effects_profile_id=['small-bluetooth-speaker-class-device'],  # Optimized for clarity
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            audio_bytes = response.audio_content
            generation_time_ms = int((time.time() - start_time) * 1000)

            # Estimate duration (22050 Hz, 16-bit mono = 44100 bytes/second)
            duration_ms = int((len(audio_bytes) / 44100) * 1000)

            logger.info(
                f"Google TTS: Generated {len(audio_bytes)} bytes, "
                f"~{duration_ms}ms audio in {generation_time_ms}ms"
            )

            return audio_bytes, duration_ms

        except Exception as e:
            logger.error(f"Google TTS error: {e}")
            raise GoogleTTSError(str(e))

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported languages."""
        return list(cls.VOICE_MAPPING.keys())

    @classmethod
    def estimate_cost(cls, text: str, use_neural: bool = False) -> float:
        """
        Estimate cost for generating audio.

        Returns cost in USD.
        """
        cost_per_char = cls.COST_PER_CHAR_NEURAL if use_neural else cls.COST_PER_CHAR_STANDARD
        return len(text) * cost_per_char

    @classmethod
    def get_provider_name(cls) -> str:
        return "google"

    @classmethod
    def list_available_voices(cls, language: str = 'HINDI') -> dict:
        """
        List available voices for a language.

        Args:
            language: Language code

        Returns:
            Dict with voice options
        """
        voice_config = cls.VOICE_MAPPING.get(language, cls.VOICE_MAPPING['HINDI'])
        return {
            'female': voice_config['voice_name'],
            'male': voice_config.get('voice_name_male'),
            'neural': voice_config.get('neural_voice'),
        }
