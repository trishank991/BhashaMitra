"""
Indian Language TTS Providers with Fallback Strategy
Primary: Indic Parler-TTS (kid-friendly voices)
Secondary: Svara TTS (kenpath/svara-tts)
Fallback: Parler TTS (parler-tts/parler_tts) for English-style voices
"""

import logging
import time
import os
import sys
import io
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SvaraTTSProvider:
    """
    Primary TTS Provider: Svara TTS via Hugging Face Spaces

    Supports: Hindi, Tamil, Telugu, Gujarati, Punjabi, Malayalam,
              Bengali, Marathi, Kannada, Odia, Assamese, Urdu
    """

    LANGUAGE_MAP = {
        'HINDI': 'Hindi (हिन्दी)',
        'TAMIL': 'Tamil (தமிழ்)',
        'GUJARATI': 'Gujarati (ગુજરાતી)',
        'PUNJABI': 'Punjabi (ਪੰਜਾਬੀ)',
        'TELUGU': 'Telugu (తెలుగు)',
        'MALAYALAM': 'Malayalam (മലയാളം)',
        'BENGALI': 'Bengali (বাংলা)',
        'MARATHI': 'Marathi (मराठी)',
        'KANNADA': 'Kannada (ಕನ್ನಡ)',
        'ODIA': 'Odia (ଓଡ଼ିଆ)',
        'ASSAMESE': 'Assamese (অসমীয়া)',
        'URDU': 'Urdu (اردو)',
    }

    SPACE_ID = "kenpath/svara-tts"
    _client = None

    @classmethod
    def _get_client(cls):
        """Lazy initialization of Gradio client."""
        if cls._client is None:
            from gradio_client import Client

            old_stdout, old_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            try:
                cls._client = Client(cls.SPACE_ID)
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr

            logger.info(f"Connected to Svara TTS Space: {cls.SPACE_ID}")
        return cls._client

    @classmethod
    def get_supported_languages(cls) -> list:
        return list(cls.LANGUAGE_MAP.keys())

    @classmethod
    def is_available(cls) -> bool:
        try:
            cls._get_client()
            return True
        except Exception:
            return False

    @classmethod
    def text_to_speech(cls, text: str, language: str = 'HINDI') -> Tuple[bytes, int]:
        start_time = time.time()

        if language not in cls.LANGUAGE_MAP:
            logger.warning(f"Language {language} not supported by Svara, falling back to Hindi")
            language = 'HINDI'

        svara_language = cls.LANGUAGE_MAP[language]

        max_retries = 3
        for attempt in range(max_retries):
            try:
                client = cls._get_client()
                result = client.predict(
                    language=svara_language,
                    gender='Female',
                    text=text,
                    api_name='/generate_speech'
                )

                if isinstance(result, str) and os.path.exists(result):
                    with open(result, 'rb') as f:
                        audio_bytes = f.read()
                    try:
                        os.remove(result)
                    except Exception:
                        pass

                    generation_time_ms = int((time.time() - start_time) * 1000)
                    logger.info(f"Svara TTS: {language}, {len(text)} chars, {len(audio_bytes)} bytes, {generation_time_ms}ms")
                    return audio_bytes, generation_time_ms
                else:
                    raise Exception(f"Unexpected result type: {type(result)}")

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"Svara TTS failed (attempt {attempt + 1}): {e}")

                # Reset client on connection errors
                if 'runtime_error' in error_msg or 'invalid state' in error_msg:
                    cls._client = None

                if 'queue' in error_msg or 'loading' in error_msg or 'busy' in error_msg:
                    time.sleep(30 * (attempt + 1))
                    continue

                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

        raise Exception("Svara TTS failed: max retries exceeded")

    @classmethod
    def get_provider_name(cls) -> str:
        return "svara"


class ParlerTTSProvider:
    """
    Fallback TTS Provider: Parler TTS (parler-tts/parler_tts)

    Note: This is primarily for English but can be used as emergency fallback.
    It won't pronounce Indian languages correctly but will produce audio.
    """

    SPACE_ID = "parler-tts/parler_tts"
    _client = None

    @classmethod
    def _get_client(cls):
        if cls._client is None:
            from gradio_client import Client

            old_stdout, old_stderr = sys.stdout, sys.stderr
            sys.stdout, sys.stderr = io.StringIO(), io.StringIO()
            try:
                cls._client = Client(cls.SPACE_ID)
            finally:
                sys.stdout, sys.stderr = old_stdout, old_stderr

            logger.info(f"Connected to Parler TTS Space: {cls.SPACE_ID}")
        return cls._client

    @classmethod
    def get_supported_languages(cls) -> list:
        return ['ENGLISH']  # Primary support is English

    @classmethod
    def is_available(cls) -> bool:
        try:
            cls._get_client()
            return True
        except Exception:
            return False

    @classmethod
    def text_to_speech(cls, text: str, language: str = 'ENGLISH') -> Tuple[bytes, int]:
        start_time = time.time()

        description = "A female speaker with a warm, engaging voice speaks clearly at a moderate pace."

        max_retries = 3
        for attempt in range(max_retries):
            try:
                client = cls._get_client()
                result = client.predict(
                    text,
                    description,
                    api_name='/gen_tts'
                )

                if isinstance(result, str) and os.path.exists(result):
                    with open(result, 'rb') as f:
                        audio_bytes = f.read()
                    try:
                        os.remove(result)
                    except Exception:
                        pass

                    generation_time_ms = int((time.time() - start_time) * 1000)
                    logger.info(f"Parler TTS: {len(text)} chars, {len(audio_bytes)} bytes, {generation_time_ms}ms")
                    return audio_bytes, generation_time_ms
                else:
                    raise Exception(f"Unexpected result type: {type(result)}")

            except Exception as e:
                error_msg = str(e).lower()
                logger.error(f"Parler TTS failed (attempt {attempt + 1}): {e}")

                if 'runtime_error' in error_msg or 'invalid state' in error_msg:
                    cls._client = None

                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

        raise Exception("Parler TTS failed: max retries exceeded")

    @classmethod
    def get_provider_name(cls) -> str:
        return "parler"


class MultiProviderTTS:
    """
    Multi-provider TTS with automatic fallback.

    Strategy:
    1. Try Indic Parler-TTS first (kid-friendly voices for Indian languages)
    2. Try Svara TTS second (reliable for Indian languages)
    3. If both fail, try Parler TTS (English fallback)
    4. Return error only if all providers fail
    """

    PROVIDERS = None  # Lazy loaded to avoid circular imports

    @classmethod
    def _get_providers(cls):
        """Lazy load providers to avoid circular imports."""
        if cls.PROVIDERS is None:
            from apps.speech.services.indic_parler_provider import IndicParlerTTSProvider
            cls.PROVIDERS = [
                IndicParlerTTSProvider,  # Primary: Kid-friendly expressive voices
                SvaraTTSProvider,         # Secondary: Reliable Indian language TTS
                ParlerTTSProvider,        # Fallback: English-style TTS
            ]
        return cls.PROVIDERS

    @classmethod
    def get_supported_languages(cls) -> list:
        """Combined list of all supported languages."""
        languages = set()
        for provider in cls._get_providers():
            languages.update(provider.get_supported_languages())
        return list(languages)

    @classmethod
    def is_available(cls) -> bool:
        """Check if at least one provider is available."""
        return any(p.is_available() for p in cls._get_providers())

    @classmethod
    def text_to_speech(cls, text: str, language: str = 'HINDI', voice_style: str = 'kid_friendly') -> Tuple[bytes, int]:
        """
        Generate speech with automatic fallback between providers.

        Args:
            text: Text to convert
            language: Language code (HINDI, TAMIL, etc.)
            voice_style: Voice style (kid_friendly, calm_story, enthusiastic)

        Returns:
            Tuple of (audio_bytes, generation_time_ms)
        """
        errors = []

        for provider in cls._get_providers():
            try:
                logger.info(f"Trying TTS provider: {provider.get_provider_name()}")
                return provider.text_to_speech(text=text, language=language)
            except Exception as e:
                error_msg = f"{provider.get_provider_name()}: {str(e)}"
                errors.append(error_msg)
                logger.warning(f"Provider {provider.get_provider_name()} failed: {e}")
                continue

        # All providers failed
        raise Exception(f"All TTS providers failed: {'; '.join(errors)}")

    @classmethod
    def get_provider_name(cls) -> str:
        return "multi"


# Main provider for backward compatibility
MMSTTSProvider = MultiProviderTTS
