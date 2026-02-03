"""
Indic Parler-TTS Provider - Kid-Friendly Voice Generation
Uses AI4Bharat's Indic Parler-TTS for expressive, engaging voices.

This provider creates voices similar to children's content creators (like Miss Rachel)
- High-pitched, cheerful voices
- Slow, clear pronunciation
- Expressive and engaging tone
- Perfect for language learning apps

Space: ai4bharat/indic-parler-tts
License: Apache 2.0 (commercially safe)
"""

import logging
import time
import os
import sys
import io
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


# Kid-friendly voice descriptions for Indic Parler-TTS
# These descriptions control how the generated speech sounds
# Inspired by Miss Rachel's engaging teaching style

KID_VOICE_PROFILES = {
    'HINDI': {
        # Primary voice - cheerful female teacher for kids
        'kid_friendly': {
            'speaker': 'Sunita',
            'description': (
                "Sunita speaks with a very high pitch in a cheerful, happy tone. "
                "She speaks slowly and clearly like a teacher talking to young children. "
                "Her voice is warm, enthusiastic, and encouraging. "
                "The recording is of excellent quality with no background noise."
            ),
        },
        # Alternative - calm bedtime story voice
        'calm_story': {
            'speaker': 'Divya',
            'description': (
                "Divya speaks with a soft, gentle voice at a slow pace. "
                "Her tone is warm and nurturing, perfect for bedtime stories. "
                "She pronounces each word very clearly. "
                "The audio is crystal clear with a peaceful quality."
            ),
        },
        # Enthusiastic - for games and exciting content
        'enthusiastic': {
            'speaker': 'Ananya',
            'description': (
                "Ananya speaks with high energy and excitement in her voice. "
                "She sounds happy and playful like she's playing a fun game. "
                "Her voice is bright and animated with expressive intonation. "
                "Very clear recording with dynamic, engaging delivery."
            ),
        },
        # Male teacher voice option
        'male_teacher': {
            'speaker': 'Rohit',
            'description': (
                "Rohit speaks with a friendly, warm male voice. "
                "He sounds like a kind teacher talking to children. "
                "His pace is slow and his pronunciation is very clear. "
                "High quality audio with an encouraging, patient tone."
            ),
        },
    },
    'TAMIL': {
        'kid_friendly': {
            'speaker': 'Priya',
            'description': (
                "Priya speaks with a high-pitched, cheerful voice. "
                "She talks slowly and clearly like a loving teacher. "
                "Her tone is warm, happy, and encouraging for children. "
                "Crystal clear recording quality."
            ),
        },
        'calm_story': {
            'speaker': 'Lakshmi',
            'description': (
                "Lakshmi speaks softly with a gentle, soothing voice. "
                "Perfect for calming stories, slow and melodic. "
                "Her pronunciation is very clear and peaceful."
            ),
        },
    },
    'GUJARATI': {
        'kid_friendly': {
            'speaker': 'Meera',
            'description': (
                "Meera speaks with a cheerful, high-pitched voice. "
                "She sounds like a happy teacher talking to children. "
                "Her pace is slow, pronunciation is very clear. "
                "Warm, encouraging tone with excellent audio quality."
            ),
        },
    },
    'PUNJABI': {
        'kid_friendly': {
            'speaker': 'Simran',
            'description': (
                "Simran speaks with a bright, cheerful voice. "
                "She talks slowly and clearly like teaching children. "
                "Her tone is warm, friendly, and encouraging. "
                "High quality clear recording."
            ),
        },
    },
    'TELUGU': {
        'kid_friendly': {
            'speaker': 'Padma',
            'description': (
                "Padma speaks with a high-pitched, happy voice. "
                "She sounds like a kind teacher for young children. "
                "Her pace is slow and pronunciation is very clear. "
                "Warm, encouraging delivery with clear audio."
            ),
        },
    },
    'MALAYALAM': {
        'kid_friendly': {
            'speaker': 'Sreelakshmi',
            'description': (
                "Sreelakshmi speaks with a cheerful, nurturing voice. "
                "She talks slowly and clearly like teaching children. "
                "Her tone is warm, happy, and encouraging. "
                "Excellent audio quality."
            ),
        },
    },
    'BENGALI': {
        'kid_friendly': {
            'speaker': 'Anindita',
            'description': (
                "Anindita speaks with a bright, happy voice. "
                "She sounds like a friendly teacher for children. "
                "Her pace is slow and very clear. "
                "Warm, encouraging tone."
            ),
        },
    },
    'MARATHI': {
        'kid_friendly': {
            'speaker': 'Sneha',
            'description': (
                "Sneha speaks with a cheerful, high-pitched voice. "
                "She talks slowly and clearly for children. "
                "Her tone is warm and encouraging. "
                "Clear audio quality."
            ),
        },
    },
}


class IndicParlerTTSProvider:
    """
    Indic Parler-TTS Provider for Kid-Friendly Voices

    Uses AI4Bharat's Indic Parler-TTS which allows natural language
    voice descriptions for expressive, controllable TTS.

    Features:
    - 69 speakers across 18+ Indian languages
    - Natural language voice control
    - High-pitched, cheerful voices for kids
    - Slow, clear pronunciation
    - Apache 2.0 license (commercially safe)

    Demo: https://huggingface.co/spaces/ai4bharat/indic-parler-tts
    """

    SPACE_ID = "ai4bharat/indic-parler-tts"
    _client = None

    # Language code mapping to Indic Parler-TTS format
    LANGUAGE_MAP = {
        'HINDI': 'hindi',
        'TAMIL': 'tamil',
        'GUJARATI': 'gujarati',
        'PUNJABI': 'punjabi',
        'TELUGU': 'telugu',
        'MALAYALAM': 'malayalam',
        'BENGALI': 'bengali',
        'MARATHI': 'marathi',
        'KANNADA': 'kannada',
        'ODIA': 'odia',
        'ASSAMESE': 'assamese',
    }

    @classmethod
    def _get_client(cls):
        """Lazy initialization of Gradio client."""
        if cls._client is None:
            from gradio_client import Client

            # Suppress gradio client output
            old_stdout, old_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            try:
                cls._client = Client(cls.SPACE_ID)
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr

            logger.info(f"Connected to Indic Parler-TTS Space: {cls.SPACE_ID}")
        return cls._client

    @classmethod
    def get_supported_languages(cls) -> list:
        """List of supported languages."""
        return list(cls.LANGUAGE_MAP.keys())

    @classmethod
    def is_available(cls) -> bool:
        """Check if the service is available."""
        try:
            cls._get_client()
            return True
        except Exception:
            return False

    @classmethod
    def get_voice_profile(cls, language: str, style: str = 'kid_friendly') -> dict:
        """
        Get the voice profile for a language and style.

        Args:
            language: Language code (HINDI, TAMIL, etc.)
            style: Voice style (kid_friendly, calm_story, enthusiastic)

        Returns:
            Dict with 'speaker' and 'description' keys
        """
        lang_profiles = KID_VOICE_PROFILES.get(language, KID_VOICE_PROFILES.get('HINDI'))
        profile = lang_profiles.get(style, lang_profiles.get('kid_friendly'))
        return profile

    @classmethod
    def text_to_speech(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_style: str = 'kid_friendly',
    ) -> Tuple[bytes, int]:
        """
        Convert text to speech using kid-friendly voice.

        Args:
            text: Text to convert (in target language script)
            language: Language code (HINDI, TAMIL, etc.)
            voice_style: Voice style (kid_friendly, calm_story, enthusiastic)

        Returns:
            Tuple of (audio_bytes, generation_time_ms)
        """
        start_time = time.time()

        if language not in cls.LANGUAGE_MAP:
            logger.warning(f"Language {language} not supported, falling back to Hindi")
            language = 'HINDI'

        parler_language = cls.LANGUAGE_MAP[language]
        voice_profile = cls.get_voice_profile(language, voice_style)
        description = voice_profile['description']

        max_retries = 3
        for attempt in range(max_retries):
            try:
                client = cls._get_client()

                # Indic Parler-TTS API call
                result = client.predict(
                    text,           # Input text
                    description,    # Voice description
                    parler_language,  # Language
                    api_name='/generate_speech'
                )

                # Handle result - could be file path or audio data
                if isinstance(result, str) and os.path.exists(result):
                    with open(result, 'rb') as f:
                        audio_bytes = f.read()
                    try:
                        os.remove(result)
                    except Exception:
                        pass
                elif isinstance(result, tuple) and len(result) >= 1:
                    # Some spaces return (sample_rate, audio_array)
                    audio_path = result[0] if isinstance(result[0], str) else result
                    if isinstance(audio_path, str) and os.path.exists(audio_path):
                        with open(audio_path, 'rb') as f:
                            audio_bytes = f.read()
                        try:
                            os.remove(audio_path)
                        except Exception:
                            pass
                    else:
                        raise Exception(f"Unexpected result format: {type(result)}")
                else:
                    raise Exception(f"Unexpected result type: {type(result)}")

                generation_time_ms = int((time.time() - start_time) * 1000)
                logger.info(
                    f"Indic Parler-TTS: {language} ({voice_style}), "
                    f"{len(text)} chars, {len(audio_bytes)} bytes, {generation_time_ms}ms"
                )
                return audio_bytes, generation_time_ms

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"Indic Parler-TTS failed (attempt {attempt + 1}): {e}")

                # Reset client on connection errors
                if 'runtime_error' in error_msg or 'invalid state' in error_msg:
                    cls._client = None

                # Wait longer on queue/busy errors
                if 'queue' in error_msg or 'loading' in error_msg or 'busy' in error_msg:
                    time.sleep(30 * (attempt + 1))
                    continue

                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

        raise Exception("Indic Parler-TTS failed: max retries exceeded")

    @classmethod
    def get_provider_name(cls) -> str:
        return "indic_parler"

    @classmethod
    def list_available_voices(cls, language: str = 'HINDI') -> list:
        """
        List available voice styles for a language.

        Args:
            language: Language code

        Returns:
            List of voice style names
        """
        lang_profiles = KID_VOICE_PROFILES.get(language, KID_VOICE_PROFILES.get('HINDI'))
        return list(lang_profiles.keys())


def get_kid_friendly_voice_description(language: str = 'HINDI', style: str = 'kid_friendly') -> str:
    """
    Helper function to get voice description for a language and style.

    This is useful for external services or testing.
    """
    return IndicParlerTTSProvider.get_voice_profile(language, style)['description']
