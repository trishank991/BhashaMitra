"""
Speech-to-Text Service for Peppi Mimic pronunciation scoring.

Supports multiple STT providers:
1. Google Cloud Speech-to-Text (primary - consistent with Google TTS)
2. Sarvam AI STT (fallback - for Indian languages)
3. Mock STT (for development/testing)

The service downloads audio from URL and transcribes it.
"""

import logging
import os
import time
import base64
import tempfile
import requests
from dataclasses import dataclass
from typing import Optional, Tuple
from urllib.parse import urlparse
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class STTResult:
    """Result of speech-to-text transcription."""
    transcription: str
    confidence: float  # 0-1
    language: str
    provider: str
    duration_ms: int


class GoogleSTTClient:
    """
    Google Cloud Speech-to-Text Client.

    Uses the same credentials as Google TTS for consistency.
    Supports both API key and service account authentication.

    API Documentation: https://cloud.google.com/speech-to-text/docs
    """

    # REST API endpoint
    API_URL = "https://speech.googleapis.com/v1/speech:recognize"

    # Language code mapping (BhashaMitra -> Google Cloud)
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
        'ODIA': 'or-IN',
        'FIJI_HINDI': 'hi-IN',  # Uses Hindi for Fiji Hindi
    }

    @classmethod
    def _get_api_key(cls) -> Optional[str]:
        """Get Google API key from settings or environment."""
        return getattr(settings, 'GOOGLE_TTS_API_KEY', None) or os.environ.get('GOOGLE_TTS_API_KEY')

    @classmethod
    def _setup_credentials_from_base64(cls) -> bool:
        """Decode base64 credentials and set up for Google Cloud SDK."""
        base64_creds = os.environ.get('GOOGLE_CREDENTIALS_BASE64')
        if not base64_creds:
            return False

        # Check if we already set up the credentials file
        existing_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if existing_path and os.path.exists(existing_path):
            return True

        try:
            # Decode and write to temp file
            creds_json = base64.b64decode(base64_creds)
            temp_file = tempfile.NamedTemporaryFile(mode='wb', suffix='.json', delete=False)
            temp_file.write(creds_json)
            temp_file.close()

            # Set environment variable for Google Cloud SDK
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = temp_file.name
            logger.info(f"Set up Google credentials from base64 at: {temp_file.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to decode Google credentials: {e}")
            return False

    @classmethod
    def is_available(cls) -> bool:
        """Check if Google Cloud STT is configured."""
        # Check for API key first (simpler auth)
        if cls._get_api_key():
            return True

        # Check for base64-encoded credentials (for cloud deployment)
        if cls._setup_credentials_from_base64():
            return True

        # Check for service account credentials file
        credentials_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            return True

        return False

    @classmethod
    def transcribe(
        cls,
        audio_url: str,
        language: str = 'HINDI',
    ) -> STTResult:
        """
        Transcribe audio from URL using Google Cloud Speech-to-Text.

        Args:
            audio_url: URL to audio file (wav, mp3, webm)
            language: Language code (HINDI, TAMIL, etc.)

        Returns:
            STTResult with transcription and confidence
        """
        api_key = cls._get_api_key()

        if api_key:
            return cls._transcribe_with_api_key(audio_url, language, api_key)
        else:
            return cls._transcribe_with_sdk(audio_url, language)

    @classmethod
    def _transcribe_with_api_key(
        cls,
        audio_url: str,
        language: str,
        api_key: str,
    ) -> STTResult:
        """Transcribe using REST API with API key."""
        start_time = time.time()

        # Map language
        target_language = cls.LANGUAGE_MAP.get(language, 'hi-IN')

        # Download audio file
        audio_data = cls._download_audio(audio_url)

        # Encode audio as base64
        audio_content_b64 = base64.b64encode(audio_data).decode('utf-8')

        # Determine encoding from URL
        parsed = urlparse(audio_url)
        ext = parsed.path.split('.')[-1].lower() if '.' in parsed.path else 'wav'

        # Map extension to Google encoding
        encoding_map = {
            'wav': 'LINEAR16',
            'mp3': 'MP3',
            'webm': 'WEBM_OPUS',
            'ogg': 'OGG_OPUS',
            'm4a': 'MP3',  # Google doesn't directly support m4a, but MP3 works for most
            'flac': 'FLAC',
        }
        encoding = encoding_map.get(ext, 'LINEAR16')

        # Build request payload
        payload = {
            "config": {
                "encoding": encoding,
                "languageCode": target_language,
                "enableAutomaticPunctuation": False,
                "model": "default",
            },
            "audio": {
                "content": audio_content_b64
            }
        }

        try:
            logger.info(f"Google STT (API Key): Transcribing audio in {language}")

            response = requests.post(
                f"{cls.API_URL}?key={api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            duration_ms = int((time.time() - start_time) * 1000)

            if response.status_code != 200:
                error_msg = response.json().get('error', {}).get('message', response.text)
                logger.error(f"Google STT API error: {response.status_code} - {error_msg}")
                raise Exception(f"Google STT API error: {error_msg}")

            result = response.json()
            results = result.get('results', [])

            if results:
                alternative = results[0].get('alternatives', [{}])[0]
                transcription = alternative.get('transcript', '')
                confidence = alternative.get('confidence', 0.8)
            else:
                transcription = ''
                confidence = 0.0

            logger.info(
                f"Google STT: {language}, transcription='{transcription[:50]}...', "
                f"confidence={confidence:.2f}, {duration_ms}ms"
            )

            return STTResult(
                transcription=transcription,
                confidence=confidence,
                language=language,
                provider='google',
                duration_ms=duration_ms
            )

        except requests.exceptions.Timeout:
            raise Exception("Google STT request timed out")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Google STT request failed: {e}")

    @classmethod
    def _transcribe_with_sdk(
        cls,
        audio_url: str,
        language: str,
    ) -> STTResult:
        """Transcribe using Google Cloud SDK with service account."""
        try:
            from google.cloud import speech
        except ImportError:
            raise Exception(
                "google-cloud-speech not installed. "
                "Run: pip install google-cloud-speech"
            )

        start_time = time.time()
        target_language = cls.LANGUAGE_MAP.get(language, 'hi-IN')

        # Download audio file
        audio_data = cls._download_audio(audio_url)

        try:
            logger.info(f"Google STT (SDK): Transcribing audio in {language}")

            client = speech.SpeechClient()

            # Determine encoding from URL
            parsed = urlparse(audio_url)
            ext = parsed.path.split('.')[-1].lower() if '.' in parsed.path else 'wav'

            # Map extension to Google encoding
            encoding_map = {
                'wav': speech.RecognitionConfig.AudioEncoding.LINEAR16,
                'mp3': speech.RecognitionConfig.AudioEncoding.MP3,
                'webm': speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                'ogg': speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
                'flac': speech.RecognitionConfig.AudioEncoding.FLAC,
            }
            encoding = encoding_map.get(ext, speech.RecognitionConfig.AudioEncoding.LINEAR16)

            audio = speech.RecognitionAudio(content=audio_data)
            config = speech.RecognitionConfig(
                encoding=encoding,
                language_code=target_language,
                enable_automatic_punctuation=False,
            )

            response = client.recognize(config=config, audio=audio)

            duration_ms = int((time.time() - start_time) * 1000)

            if response.results:
                alternative = response.results[0].alternatives[0]
                transcription = alternative.transcript
                confidence = alternative.confidence
            else:
                transcription = ''
                confidence = 0.0

            logger.info(
                f"Google STT: {language}, transcription='{transcription[:50]}...', "
                f"confidence={confidence:.2f}, {duration_ms}ms"
            )

            return STTResult(
                transcription=transcription,
                confidence=confidence,
                language=language,
                provider='google',
                duration_ms=duration_ms
            )

        except Exception as e:
            logger.error(f"Google STT SDK error: {e}")
            raise Exception(f"Google STT error: {e}")

    @classmethod
    def _download_audio(cls, url: str) -> bytes:
        """
        Get audio content from URL or local file.

        For local media URLs (containing /media/), reads directly from disk
        to avoid HTTP timeout issues when server downloads from itself.
        """
        # Check if this is a local media URL
        if '/media/' in url:
            try:
                # Extract relative path from URL
                # URL: https://bhashamitra.onrender.com/media/mimic_recordings/xxx/yyy.webm
                # Relative path: mimic_recordings/xxx/yyy.webm
                relative_path = url.split('/media/')[-1]
                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)

                if os.path.exists(file_path):
                    logger.info(f"Reading audio from local file: {file_path}")
                    with open(file_path, 'rb') as f:
                        return f.read()
                else:
                    logger.warning(f"Local file not found: {file_path}, falling back to HTTP")
            except Exception as e:
                logger.warning(f"Failed to read local file, falling back to HTTP: {e}")

        # Fall back to HTTP download for external URLs or if local read failed
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Failed to download audio from {url}: {e}")


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
        model: str = 'saarika:v2.5'
    ) -> STTResult:
        """
        Transcribe audio from URL using Sarvam AI STT.

        Args:
            audio_url: URL to audio file (wav, mp3, webm)
            language: Language code (HINDI, TAMIL, etc.)
            model: Sarvam model (default: saarika:v2.5)

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
        """
        Get audio content from URL or local file.

        For local media URLs (containing /media/), reads directly from disk
        to avoid HTTP timeout issues when server downloads from itself.
        """
        # Check if this is a local media URL
        if '/media/' in url:
            try:
                # Extract relative path from URL
                relative_path = url.split('/media/')[-1]
                file_path = os.path.join(settings.MEDIA_ROOT, relative_path)

                if os.path.exists(file_path):
                    logger.info(f"Reading audio from local file: {file_path}")
                    with open(file_path, 'rb') as f:
                        return f.read()
                else:
                    logger.warning(f"Local file not found: {file_path}, falling back to HTTP")
            except Exception as e:
                logger.warning(f"Failed to read local file, falling back to HTTP: {e}")

        # Fall back to HTTP download for external URLs or if local read failed
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            return response.content
        except Exception as e:
            raise Exception(f"Failed to download audio from {url}: {e}")


class MockSTTClient:
    """
    Mock STT client for development/testing ONLY.
    
    WARNING: This should NEVER be used in production!
    It returns fake "perfect" results that give children false confidence.
    
    In production, this class will raise an error if accessed.
    """

    @classmethod
    def is_available(cls) -> bool:
        """
        Mock is available only in development mode.
        
        In production (DJANGO_ENV=prod), this returns False to prevent
        accidental use of fake transcription results.
        """
        import os
        from django.conf import settings
        
        # Only available in development mode
        django_env = getattr(settings, 'DJANGO_ENV', 'dev')
        return django_env != 'prod'

    @classmethod
    def transcribe(
        cls,
        audio_url: str,
        language: str = 'HINDI',
        expected_word: Optional[str] = None
    ) -> STTResult:
        """
        Return mock transcription result for development/testing ONLY.
        
        Raises:
            RuntimeError: If called in production mode
        """
        if not cls.is_available():
            raise RuntimeError(
                "MOCK STT IS NOT AVAILABLE IN PRODUCTION!\n"
                "This is a security/safety feature to prevent false scoring.\n"
                "Please configure GOOGLE_TTS_API_KEY or SARVAM_API_KEY for STT."
            )

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

        logger.warning(
            f"? MOCK STT ACTIVE - This is for TESTING only! "
            f"transcription='{transcription}', confidence={confidence:.2f}"
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

    Priority (consistent with TTS):
    1. Google Cloud STT (primary - consistent with Google TTS)
    2. Sarvam AI STT (fallback for Indian languages)
    3. Mock STT (development/testing fallback)
    """

    @classmethod
    def get_provider(cls) -> str:
        """Get the name of the active STT provider."""
        if GoogleSTTClient.is_available():
            return 'google'
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
        # Try Google Cloud STT first (consistent with Google TTS)
        if GoogleSTTClient.is_available():
            try:
                return GoogleSTTClient.transcribe(audio_url, language)
            except Exception as e:
                logger.warning(f"Google STT failed, falling back to Sarvam: {e}")

        # Try Sarvam AI as fallback
        if SarvamSTTClient.is_available():
            try:
                return SarvamSTTClient.transcribe(audio_url, language)
            except Exception as e:
                logger.warning(f"Sarvam STT failed, falling back to mock: {e}")

        # Fallback to mock
        return MockSTTClient.transcribe(audio_url, language, expected_word)


# Default instance
stt_service = STTService()