"""
Sarvam AI TTS Provider for BhashaMitra Premium Tier.

Uses Sarvam AI Bulbul V2 model for human-like Indian language voices.
API Documentation: https://docs.sarvam.ai/api-reference-docs/endpoints/text-to-speech
"""

import logging
import time
import os
import base64
import requests
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class SarvamAIProvider:
    """
    Premium TTS Provider: Sarvam AI Bulbul V2

    High-quality, human-like voices for Indian languages.
    Used for Premium tier members ($20/month).

    Supports: Hindi, Tamil, Telugu, Kannada, Malayalam,
              Gujarati, Marathi, Bengali, Punjabi, Odia
    """

    API_ENDPOINT = "https://api.sarvam.ai/text-to-speech"

    # Language code mapping (BhashaMitra -> Sarvam AI)
    LANGUAGE_MAP = {
        'HINDI': 'hi-IN',
        'TAMIL': 'ta-IN',
        'TELUGU': 'te-IN',
        'KANNADA': 'kn-IN',
        'MALAYALAM': 'ml-IN',
        'GUJARATI': 'gu-IN',
        'MARATHI': 'mr-IN',
        'BENGALI': 'bn-IN',
        'PUNJABI': 'pa-IN',
        'ODIA': 'od-IN',
    }

    # Available voices for Bulbul v2 model
    VOICES = {
        'anushka': {'gender': 'female', 'style': 'warm', 'best_for': 'storytelling, kids content'},
        'manisha': {'gender': 'female', 'style': 'clear', 'best_for': 'instructions, educational'},
        'vidya': {'gender': 'female', 'style': 'expressive', 'best_for': 'enthusiastic content'},
        'arya': {'gender': 'female', 'style': 'friendly', 'best_for': 'general content'},
        'abhilash': {'gender': 'male', 'style': 'friendly', 'best_for': 'male teacher voice'},
        'karun': {'gender': 'male', 'style': 'professional', 'best_for': 'formal content'},
        'hitesh': {'gender': 'male', 'style': 'casual', 'best_for': 'conversational'},
    }

    # Default voice for kid-friendly content (Dec 2024: manisha selected for clear, energetic style)
    DEFAULT_VOICE = 'manisha'
    DEFAULT_MALE_VOICE = 'abhilash'

    # Speech pace control (1.0 = normal, <1.0 = slower, >1.0 = faster)
    # Slightly slower for clarity but natural enough to sound clear
    DEFAULT_PACE = 0.85  # 85% speed - clear but natural sounding

    @classmethod
    def _get_api_key(cls) -> Optional[str]:
        """Get Sarvam API key from environment."""
        return os.environ.get('SARVAM_API_KEY')

    @classmethod
    def get_supported_languages(cls) -> list:
        """Return list of supported language codes."""
        return list(cls.LANGUAGE_MAP.keys())

    @classmethod
    def is_available(cls) -> bool:
        """Check if Sarvam AI is configured and available."""
        api_key = cls._get_api_key()
        return api_key is not None and len(api_key) > 0

    @classmethod
    def get_available_voices(cls) -> dict:
        """Return available voice options with metadata."""
        return cls.VOICES

    @classmethod
    def text_to_speech(
        cls,
        text: str,
        language: str = 'HINDI',
        voice: str = None,
        model: str = 'bulbul:v2',
        pace: float = None
    ) -> Tuple[bytes, int]:
        """
        Generate speech using Sarvam AI Bulbul V2.

        Args:
            text: Text to convert to speech
            language: Language code (HINDI, TAMIL, etc.)
            voice: Voice name (meera, pavithra, maitreyi, arvind)
            model: Model name (default: bulbul:v2)
            pace: Speech speed (1.0 = normal, <1.0 = slower, >1.0 = faster)

        Returns:
            Tuple of (audio_bytes, generation_time_ms)

        Raises:
            Exception: If API call fails or language not supported
        """
        start_time = time.time()

        # Validate API key
        api_key = cls._get_api_key()
        if not api_key:
            raise Exception("SARVAM_API_KEY not configured")

        # Map language to Sarvam format
        if language not in cls.LANGUAGE_MAP:
            logger.warning(f"Language {language} not supported by Sarvam AI, falling back to Hindi")
            language = 'HINDI'

        target_language = cls.LANGUAGE_MAP[language]

        # Use default voice if not specified
        if voice is None:
            voice = cls.DEFAULT_VOICE

        # Validate voice
        if voice not in cls.VOICES:
            logger.warning(f"Voice {voice} not available, using default: {cls.DEFAULT_VOICE}")
            voice = cls.DEFAULT_VOICE

        # Use default pace if not specified (slightly slower for kids content)
        if pace is None:
            pace = cls.DEFAULT_PACE

        # Prepare request
        headers = {
            'API-Subscription-Key': api_key,
            'Content-Type': 'application/json',
        }

        payload = {
            'inputs': [text],
            'target_language_code': target_language,
            'speaker': voice,
            'model': model,
            'pace': pace,  # Speech speed: <1.0 = slower, 1.0 = normal, >1.0 = faster
        }

        # Make API request with retry
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.post(
                    cls.API_ENDPOINT,
                    headers=headers,
                    json=payload,
                    timeout=60  # 60 second timeout
                )

                if response.status_code == 200:
                    # API returns JSON with base64-encoded audio
                    data = response.json()
                    audio_base64 = data['audios'][0]
                    audio_bytes = base64.b64decode(audio_base64)
                    generation_time_ms = int((time.time() - start_time) * 1000)

                    logger.info(
                        f"Sarvam AI TTS: {language}, {len(text)} chars, "
                        f"{len(audio_bytes)} bytes, {generation_time_ms}ms, voice={voice}, pace={pace}"
                    )

                    return audio_bytes, generation_time_ms

                elif response.status_code == 401:
                    raise Exception("Invalid Sarvam API key")

                elif response.status_code == 429:
                    # Rate limited - wait and retry
                    wait_time = 5 * (attempt + 1)
                    logger.warning(f"Sarvam AI rate limited, waiting {wait_time}s")
                    time.sleep(wait_time)
                    continue

                else:
                    error_msg = f"Sarvam AI API error: {response.status_code}"
                    try:
                        error_detail = response.json()
                        error_msg += f" - {error_detail}"
                    except:
                        pass
                    raise Exception(error_msg)

            except requests.exceptions.Timeout:
                logger.error(f"Sarvam AI timeout (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    raise Exception("Sarvam AI request timed out")
                time.sleep(2)

            except requests.exceptions.RequestException as e:
                logger.error(f"Sarvam AI request failed: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2)

        raise Exception("Sarvam AI failed: max retries exceeded")

    @classmethod
    def get_provider_name(cls) -> str:
        """Return provider identifier."""
        return "sarvam"

    @classmethod
    def estimate_cost(cls, text: str) -> float:
        """
        Estimate cost for generating speech for given text.

        Sarvam AI pricing (approximate):
        - ~$0.0001 per character

        Args:
            text: Text to estimate cost for

        Returns:
            Estimated cost in USD
        """
        char_count = len(text)
        cost_per_char = 0.0001  # $0.0001 per character (approximate)
        return char_count * cost_per_char
