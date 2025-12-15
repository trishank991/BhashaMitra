"""
Hugging Face Spaces Gradio API client for TTS.
Uses the Parler-TTS Space for high-quality text-to-speech.
"""
import time
import logging
import tempfile
import os
from typing import Optional, Tuple
from django.conf import settings

logger = logging.getLogger(__name__)


class HuggingFaceInferenceError(Exception):
    """Custom exception for HF API errors"""
    pass


class HuggingFaceClient:
    """
    Client for Hugging Face Spaces API using Gradio.

    Uses the parler-tts Space for TTS generation.
    Free tier available, PRO recommended for better rate limits.
    """

    # Default Spaces to use
    PARLER_TTS_SPACE = "parler-tts/parler_tts"
    INDIC_PARLER_TTS_SPACE = "ai4bharat/indic-parler-tts"

    def __init__(self):
        self.api_token = getattr(settings, 'HUGGINGFACE_API_TOKEN', '')
        self.space_id = getattr(settings, 'TTS_SPACE_ID', self.PARLER_TTS_SPACE)
        self._client = None

    def _get_client(self):
        """Lazy initialization of Gradio client."""
        if self._client is None:
            try:
                from gradio_client import Client
                import sys
                import io
                import os

                # Set HF token in environment for authentication
                if self.api_token:
                    os.environ['HF_TOKEN'] = self.api_token

                # Suppress gradio client output on Windows (encoding issues)
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = io.StringIO()
                sys.stderr = io.StringIO()

                try:
                    # Connect to the Hugging Face Space
                    self._client = Client(self.space_id)
                finally:
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

                logger.info(f"Connected to Gradio Space: {self.space_id}")
            except Exception as e:
                logger.error(f"Failed to connect to Space {self.space_id}: {e}")
                raise HuggingFaceInferenceError(f"Failed to connect to TTS Space: {e}")
        return self._client

    def text_to_speech(
        self,
        text: str,
        description: str,
        max_retries: int = 3,
        timeout: int = 120
    ) -> bytes:
        """
        Generate speech from text using Parler-TTS Space.

        Args:
            text: The text to convert to speech
            description: Voice description (controls voice characteristics)
            max_retries: Number of retry attempts
            timeout: Request timeout in seconds

        Returns:
            Audio bytes (WAV format)

        Raises:
            HuggingFaceInferenceError: If generation fails
        """
        # Different Spaces may have different API endpoint names
        api_names = ["/gen_tts", "/predict", "/synthesize", "/generate"]

        for attempt in range(max_retries):
            try:
                start_time = time.time()
                client = self._get_client()

                result = None
                last_error = None

                # Try different API endpoints
                for api_name in api_names:
                    try:
                        result = client.predict(
                            text,           # Text to synthesize
                            description,    # Voice description
                            api_name=api_name
                        )
                        logger.info(f"Successfully used API endpoint: {api_name}")
                        break
                    except Exception as api_err:
                        last_error = api_err
                        if "api_name" in str(api_err).lower() or "not found" in str(api_err).lower():
                            continue
                        else:
                            raise

                if result is None:
                    raise last_error or HuggingFaceInferenceError("No valid API endpoint found")

                elapsed_ms = int((time.time() - start_time) * 1000)

                # Result is typically a file path to the generated audio
                audio_bytes = self._extract_audio_from_result(result)
                if audio_bytes:
                    logger.info(f"TTS generated in {elapsed_ms}ms for {len(text)} chars")
                    return audio_bytes
                else:
                    raise HuggingFaceInferenceError(f"Unexpected result type: {type(result)}")

            except Exception as e:
                error_msg = str(e).lower()
                logger.warning(f"TTS attempt {attempt + 1}/{max_retries} failed: {e}")

                # Check for rate limiting
                if 'rate' in error_msg or 'limit' in error_msg or 'quota' in error_msg:
                    wait_time = 60 * (attempt + 1)
                    logger.warning(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                # Check for queue/loading issues
                if 'queue' in error_msg or 'loading' in error_msg or 'busy' in error_msg:
                    wait_time = 30 * (attempt + 1)
                    logger.info(f"Space busy. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                if attempt == max_retries - 1:
                    raise HuggingFaceInferenceError(f"TTS generation failed: {e}")

                time.sleep(5)  # Brief pause before retry

        raise HuggingFaceInferenceError("Max retries exceeded")

    def _extract_audio_from_result(self, result) -> Optional[bytes]:
        """Extract audio bytes from various result formats."""
        # Handle string path
        if isinstance(result, str) and os.path.exists(result):
            with open(result, 'rb') as f:
                audio_bytes = f.read()
            try:
                os.remove(result)
            except Exception:
                pass
            return audio_bytes

        # Handle tuple (some Spaces return tuple with file path)
        if isinstance(result, tuple) and len(result) > 0:
            for item in result:
                if isinstance(item, str) and os.path.exists(item):
                    with open(item, 'rb') as f:
                        audio_bytes = f.read()
                    try:
                        os.remove(item)
                    except Exception:
                        pass
                    return audio_bytes

        # Handle dict with file path
        if isinstance(result, dict):
            for key in ['audio', 'file', 'path', 'output']:
                if key in result:
                    path = result[key]
                    if isinstance(path, str) and os.path.exists(path):
                        with open(path, 'rb') as f:
                            audio_bytes = f.read()
                        try:
                            os.remove(path)
                        except Exception:
                            pass
                        return audio_bytes

        return None

    def text_to_speech_simple(
        self,
        text: str,
        description: str = "A female speaker with a warm, engaging voice speaks clearly."
    ) -> Tuple[bytes, int]:
        """
        Simplified TTS method that returns audio bytes and generation time.

        Returns:
            Tuple of (audio_bytes, generation_time_ms)
        """
        start_time = time.time()
        audio_bytes = self.text_to_speech(text, description)
        elapsed_ms = int((time.time() - start_time) * 1000)
        return audio_bytes, elapsed_ms

    def check_model_status(self) -> dict:
        """Check if the TTS Space is available."""
        try:
            client = self._get_client()
            return {
                "status": "ready",
                "space": self.space_id,
                "note": "Space connected successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "space": self.space_id,
                "message": str(e)
            }

    def get_usage_stats(self) -> dict:
        """Get current usage statistics."""
        return {
            "account_type": getattr(settings, 'HUGGINGFACE_ACCOUNT_TYPE', 'unknown'),
            "space": self.space_id,
            "note": "Check https://huggingface.co/settings/billing for exact usage"
        }
