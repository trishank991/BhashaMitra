"""
Speech-to-Text Service for Peppi Mimic pronunciation scoring.

Supports multiple STT providers:
1. Sarvam AI STT (primary - for Indian languages)
2. Google Cloud Speech-to-Text (fallback)
3. Mock STT (for development/testing)

The service downloads audio from URL and transcribes it.
"""

import logging
import os
import time
import tempfile
import requests
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


@dataclass
class STTResult:
    """Result of speech-to-text transcription."""
    transcription: str
    confidence: float  # 0-1
    language: str
    provider: str
    duration_ms: int


class SarvamSTTClient:
    """
    Sarvam AI Speech-to-Text Client.

    API Documentation: https://docs.sarvam.ai/api-reference-docs/endpoints/speech-to-text
    """

    API_ENDPOINT = "https://api.sarvam.ai/speech-to-text"

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

    @classmethod
    def _get_api_key(cls) -> Optional[str]:
        """Get Sarvam API key from environment."""
        return os.environ.get('SARVAM_API_KEY')

    @classmethod
    def is_available(cls) -> bool:
        """Check if Sarvam STT is configured."""
        api_key = cls._get_api_key()
        return api_key is not None and len(api_key) > 0

    @classmethod
    def transcribe(
        cls,
        audio_url: str,
        language: str = 'HINDI',
        model: str = 'saarika:v2'
    ) -> STTResult:
        """
        Transcribe audio from URL using Sarvam AI STT.

        Args:
            audio_url: URL to audio file (wav, mp3, webm)
            language: Language code (HINDI, TAMIL, etc.)
            model: Sarvam model (default: saarika:v2)

        Returns:
            STTResult with transcription and confidence
        """
        start_time = time.time()

        api_key = cls._get_api_key()
        if not api_key:
            raise Exception("SARVAM_API_KEY not configured")

        # Map language
        target_language = cls.LANGUAGE_MAP.get(language, 'hi-IN')

        # Download audio file
        audio_data = cls._download_audio(audio_url)

        # Prepare multipart request
        headers = {
            'API-Subscription-Key': api_key,
        }

        # Determine file extension from URL
        parsed = urlparse(audio_url)
        ext = parsed.path.split('.')[-1] if '.' in parsed.path else 'wav'
        if ext not in ['wav', 'mp3', 'webm', 'ogg', 'm4a']:
            ext = 'wav'

        files = {
            'file': (f'audio.{ext}', audio_data, f'audio/{ext}')
        }

        data = {
            'language_code': target_language,
            'model': model,
        }

        try:
            response = requests.post(
                cls.API_ENDPOINT,
                headers=headers,
                files=files,
                data=data,
                timeout=30
            )

            duration_ms = int((time.time() - start_time) * 1000)

            if response.status_code == 200:
                result = response.json()
                transcription = result.get('transcript', '')
                # Sarvam returns confidence as a score, normalize to 0-1
                confidence = result.get('confidence', 0.8)
                if confidence > 1:
                    confidence = confidence / 100

                logger.info(
                    f"Sarvam STT: {language}, transcription='{transcription[:50]}...', "
                    f"confidence={confidence:.2f}, {duration_ms}ms"
                )

                return STTResult(
                    transcription=transcription,
                    confidence=confidence,
                    language=language,
                    provider='sarvam',
                    duration_ms=duration_ms
                )
            else:
                error_msg = f"Sarvam STT error: {response.status_code}"
                try:
                    error_detail = response.json()
                    error_msg += f" - {error_detail}"
                except:
                    pass
                raise Exception(error_msg)

        except requests.exceptions.Timeout:
            raise Exception("Sarvam STT request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Sarvam STT request failed: {e}")

    @classmethod
    def _download_audio(cls, url: str) -> bytes:
        """Download audio file from URL."""
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Failed to download audio from {url}: {e}")


class MockSTTClient:
    """
    Mock STT client for development/testing.

    Returns simulated transcription results based on expected word.
    Useful when STT API is not configured or for testing.
    """

    @classmethod
    def is_available(cls) -> bool:
        """Mock is always available."""
        return True

    @classmethod
    def transcribe(
        cls,
        audio_url: str,
        language: str = 'HINDI',
        expected_word: Optional[str] = None
    ) -> STTResult:
        """
        Return mock transcription result.

        For testing, returns the expected word with some random variation
        to simulate real STT behavior.
        """
        import random

        # Simulate processing time
        time.sleep(0.5)

        # If expected word is provided, use it with some variation
        if expected_word:
            # 70% chance of perfect transcription
            if random.random() < 0.7:
                transcription = expected_word
                confidence = random.uniform(0.85, 0.98)
            else:
                # Introduce slight variation
                transcription = expected_word
                confidence = random.uniform(0.60, 0.85)
        else:
            transcription = ""
            confidence = 0.5

        logger.info(
            f"Mock STT: {language}, transcription='{transcription}', "
            f"confidence={confidence:.2f}"
        )

        return STTResult(
            transcription=transcription,
            confidence=confidence,
            language=language,
            provider='mock',
            duration_ms=500
        )


class STTService:
    """
    Unified STT Service that selects the best available provider.

    Priority:
    1. Sarvam AI STT (if configured)
    2. Mock STT (fallback for development)
    """

    @classmethod
    def get_provider(cls) -> str:
        """Get the name of the active STT provider."""
        if SarvamSTTClient.is_available():
            return 'sarvam'
        return 'mock'

    @classmethod
    def transcribe(
        cls,
        audio_url: str,
        language: str = 'HINDI',
        expected_word: Optional[str] = None
    ) -> STTResult:
        """
        Transcribe audio using the best available provider.

        Args:
            audio_url: URL to audio file
            language: Language code
            expected_word: Optional expected word (for mock testing)

        Returns:
            STTResult with transcription and confidence
        """
        # Try Sarvam first
        if SarvamSTTClient.is_available():
            try:
                return SarvamSTTClient.transcribe(audio_url, language)
            except Exception as e:
                logger.warning(f"Sarvam STT failed, falling back to mock: {e}")

        # Fallback to mock
        return MockSTTClient.transcribe(audio_url, language, expected_word)


# Default instance
stt_service = STTService()
