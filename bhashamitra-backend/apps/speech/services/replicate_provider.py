"""
Replicate.com TTS Provider
Uses Facebook MMS-TTS for Indian languages via serverless GPU

Cost: ~$0.0023/second GPU time (~$0.01-0.02 per audio clip)
"""
import os
import logging
import time
import requests
from typing import Tuple, Optional

logger = logging.getLogger(__name__)


class ReplicateTTSError(Exception):
    """Replicate TTS specific error."""
    pass


class ReplicateTTSProvider:
    """
    Serverless TTS using Replicate.com

    Supported languages:
    - Hindi (hin)
    - Tamil (tam)
    - Telugu (tel)
    - Gujarati (guj)
    - Punjabi (pan)
    - Malayalam (mal)
    - Bengali (ben)
    - Kannada (kan)

    Uses Facebook MMS-TTS model for high-quality Indian language TTS.
    """

    # Language to MMS model language code mapping
    LANGUAGE_CODES = {
        'HINDI': 'hin',
        'TAMIL': 'tam',
        'TELUGU': 'tel',
        'GUJARATI': 'guj',
        'PUNJABI': 'pan',
        'MALAYALAM': 'mal',
        'BENGALI': 'ben',
        'KANNADA': 'kan',
        'MARATHI': 'mar',
        'ODIA': 'ory',
        'ASSAMESE': 'asm',
    }

    # Replicate model - using Facebook MMS-TTS
    # Alternative models to try if this doesn't work:
    # - "facebook/mms-tts" (official)
    # - "cjwbw/mms-tts" (community hosted)
    MODEL_ID = "lucataco/xtts-v2:684bc3855b37866c0c65add2ff39c78f3dea3f4ff103a436465326e0f438d55e"

    # Fallback to simpler model
    FALLBACK_MODEL_ID = "suno-ai/bark:b76242b40d67c76ab6742e987628a2a9ac019e11d56ab96c4e91ce03b79b2787"

    @classmethod
    def is_available(cls) -> bool:
        """Check if Replicate is configured and available."""
        return bool(os.environ.get('REPLICATE_API_TOKEN'))

    @classmethod
    def generate(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_profile: str = 'default',
    ) -> Tuple[bytes, int]:
        """
        Generate TTS audio using Replicate.

        Args:
            text: Text to convert to speech
            language: Language code (HINDI, TAMIL, etc.)
            voice_profile: Voice style (not fully supported yet)

        Returns:
            Tuple of (audio_bytes, duration_ms)

        Raises:
            ReplicateTTSError: If generation fails
        """
        try:
            import replicate
        except ImportError:
            raise ReplicateTTSError("replicate package not installed. Run: pip install replicate")

        api_token = os.environ.get('REPLICATE_API_TOKEN')
        if not api_token:
            raise ReplicateTTSError("REPLICATE_API_TOKEN not configured")

        lang_code = cls.LANGUAGE_CODES.get(language, 'hin')
        start_time = time.time()

        try:
            logger.info(f"Replicate TTS: Generating audio for '{text[:50]}...' in {language}")

            # Try XTTS-v2 first (better quality, multilingual)
            try:
                output = replicate.run(
                    cls.MODEL_ID,
                    input={
                        "text": text,
                        "language": "hi" if language == "HINDI" else lang_code[:2],  # XTTS uses 2-letter codes
                        "speaker": "https://replicate.delivery/pbxt/Jt79w0xsT64R1JsiJ0LQRL8UcWspg5J4RFrU6YwEKpOT1ukS/male.wav",
                    }
                )
            except Exception as e:
                logger.warning(f"XTTS-v2 failed, trying Bark: {e}")
                # Fallback to Bark (simpler but works)
                output = replicate.run(
                    cls.FALLBACK_MODEL_ID,
                    input={
                        "prompt": text,
                        "text_temp": 0.7,
                        "waveform_temp": 0.7,
                    }
                )

            # Output is typically a URL to the generated audio
            if isinstance(output, str):
                audio_url = output
            elif hasattr(output, 'url'):
                audio_url = output.url
            elif isinstance(output, list) and len(output) > 0:
                audio_url = output[0] if isinstance(output[0], str) else str(output[0])
            elif hasattr(output, '__iter__'):
                # Iterator output from replicate
                audio_url = None
                for item in output:
                    if isinstance(item, str):
                        audio_url = item
                        break
                if not audio_url:
                    raise ReplicateTTSError(f"Could not extract URL from output")
            else:
                raise ReplicateTTSError(f"Unexpected output format: {type(output)}")

            # Download the audio
            response = requests.get(audio_url, timeout=60)
            response.raise_for_status()
            audio_bytes = response.content

            # Calculate duration
            generation_time_ms = int((time.time() - start_time) * 1000)

            # Estimate audio duration (rough calculation for WAV/MP3)
            # More accurate would be to use pydub
            duration_ms = len(audio_bytes) // 44  # Approximate for 22kHz mono

            logger.info(f"Replicate TTS: Generated {len(audio_bytes)} bytes in {generation_time_ms}ms")

            return audio_bytes, duration_ms

        except requests.RequestException as e:
            logger.error(f"Failed to download audio from Replicate: {e}")
            raise ReplicateTTSError(f"Failed to download audio: {e}")
        except Exception as e:
            logger.error(f"Replicate TTS error: {e}")
            raise ReplicateTTSError(str(e))

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported languages."""
        return list(cls.LANGUAGE_CODES.keys())

    @classmethod
    def estimate_cost(cls, text: str) -> float:
        """
        Estimate cost for generating audio.

        Returns cost in USD.
        Replicate charges ~$0.0023/second of GPU time.
        Average generation takes ~5-10 seconds.
        """
        # Approximate: 1 second of audio per 10 characters
        # GPU time is roughly proportional
        estimated_gpu_seconds = max(5, len(text) / 10)
        return estimated_gpu_seconds * 0.0023

    @classmethod
    def get_provider_name(cls) -> str:
        return "replicate"
