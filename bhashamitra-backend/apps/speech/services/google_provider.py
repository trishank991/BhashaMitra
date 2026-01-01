"""
Google Cloud TTS Provider
High-quality commercial TTS for Indian languages.

Supports two authentication methods:
1. API Key (GOOGLE_TTS_API_KEY) - Simple REST API
2. Service Account (GOOGLE_APPLICATION_CREDENTIALS) - Full SDK

Cost: ~$4 per 1 million characters (Standard voices)
      ~$16 per 1 million characters (WaveNet/Neural voices)

Used for: STANDARD tier ($20/month) and PREMIUM tier ($30/month)
"""
import os
import base64
import logging
import time
import requests
from typing import Tuple, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


class GoogleTTSError(Exception):
    """Google TTS specific error."""
    pass


class GoogleTTSProvider:
    """
    Google Cloud Text-to-Speech Provider

    Supported Indian languages:
    - Hindi (hi-IN) - Standard + WaveNet
    - Tamil (ta-IN) - Standard + WaveNet
    - Telugu (te-IN) - Standard + WaveNet
    - Gujarati (gu-IN) - Standard
    - Malayalam (ml-IN) - Standard
    - Bengali (bn-IN) - Standard + WaveNet
    - Kannada (kn-IN) - Standard
    - Marathi (mr-IN) - Standard
    - Punjabi (pa-IN) - Standard

    Voice Types:
    - Standard: Good quality, cheaper ($4/M chars)
    - WaveNet: High quality, more natural ($16/M chars) - PREMIUM only
    """

    # REST API endpoint
    API_URL = "https://texttospeech.googleapis.com/v1/text:synthesize"

    # Language to Google voice mapping with WaveNet options
    # NOTE: Uses hi-IN-*-A voices (child-friendly, matches Peppi voice)
    VOICE_MAPPING = {
        'FIJI_HINDI': {
            'language_code': 'hi-IN',  # Uses Hindi TTS
            'voice_name': 'hi-IN-Standard-A',  # Female, child-friendly (Peppi voice)
            'voice_name_male': 'hi-IN-Standard-B',
            'wavenet_voice': 'hi-IN-Wavenet-A',  # High quality female (Peppi voice)
            'wavenet_voice_male': 'hi-IN-Wavenet-B',
        },
        'HINDI': {
            'language_code': 'hi-IN',
            'voice_name': 'hi-IN-Standard-A',  # Female, child-friendly (Peppi voice)
            'voice_name_male': 'hi-IN-Standard-B',
            'wavenet_voice': 'hi-IN-Wavenet-A',  # High quality female (Peppi voice)
            'wavenet_voice_male': 'hi-IN-Wavenet-B',
        },
        'TAMIL': {
            'language_code': 'ta-IN',
            'voice_name': 'ta-IN-Standard-D',
            'voice_name_male': 'ta-IN-Standard-C',
            'wavenet_voice': 'ta-IN-Wavenet-D',
            'wavenet_voice_male': 'ta-IN-Wavenet-C',
        },
        'TELUGU': {
            'language_code': 'te-IN',
            'voice_name': 'te-IN-Standard-B',
            'voice_name_male': 'te-IN-Standard-A',
            'wavenet_voice': None,  # Not available yet
        },
        'GUJARATI': {
            'language_code': 'gu-IN',
            'voice_name': 'gu-IN-Standard-B',
            'voice_name_male': 'gu-IN-Standard-A',
            'wavenet_voice': 'gu-IN-Wavenet-B',
            'wavenet_voice_male': 'gu-IN-Wavenet-A',
        },
        'MALAYALAM': {
            'language_code': 'ml-IN',
            'voice_name': 'ml-IN-Standard-B',
            'voice_name_male': 'ml-IN-Standard-A',
            'wavenet_voice': 'ml-IN-Wavenet-D',
            'wavenet_voice_male': 'ml-IN-Wavenet-C',
        },
        'BENGALI': {
            'language_code': 'bn-IN',
            'voice_name': 'bn-IN-Standard-B',
            'voice_name_male': 'bn-IN-Standard-A',
            'wavenet_voice': 'bn-IN-Wavenet-B',
            'wavenet_voice_male': 'bn-IN-Wavenet-A',
        },
        'KANNADA': {
            'language_code': 'kn-IN',
            'voice_name': 'kn-IN-Standard-B',
            'voice_name_male': 'kn-IN-Standard-A',
            'wavenet_voice': 'kn-IN-Wavenet-B',
            'wavenet_voice_male': 'kn-IN-Wavenet-A',
        },
        'MARATHI': {
            'language_code': 'mr-IN',
            'voice_name': 'mr-IN-Standard-B',
            'voice_name_male': 'mr-IN-Standard-A',
            'wavenet_voice': 'mr-IN-Wavenet-B',
            'wavenet_voice_male': 'mr-IN-Wavenet-A',
        },
        'PUNJABI': {
            'language_code': 'pa-IN',
            'voice_name': 'pa-IN-Standard-B',
            'voice_name_male': 'pa-IN-Standard-A',
            'wavenet_voice': 'pa-IN-Wavenet-D',
            'wavenet_voice_male': 'pa-IN-Wavenet-C',
        },
        'ODIA': {
            # Odia uses Hindi fallback (no native Google TTS yet)
            'language_code': 'hi-IN',
            'voice_name': 'hi-IN-Standard-A',
            'voice_name_male': 'hi-IN-Standard-B',
            'wavenet_voice': 'hi-IN-Wavenet-A',
            'wavenet_voice_male': 'hi-IN-Wavenet-B',
        },
        'ASSAMESE': {
            # Assamese uses Bengali as closest linguistic relative
            'language_code': 'bn-IN',
            'voice_name': 'bn-IN-Standard-B',
            'voice_name_male': 'bn-IN-Standard-A',
            'wavenet_voice': 'bn-IN-Wavenet-B',
            'wavenet_voice_male': 'bn-IN-Wavenet-A',
        },
        'URDU': {
            # Urdu has limited support, uses Hindi with similar pronunciation
            'language_code': 'hi-IN',
            'voice_name': 'hi-IN-Standard-A',
            'voice_name_male': 'hi-IN-Standard-B',
            'wavenet_voice': 'hi-IN-Wavenet-A',
            'wavenet_voice_male': 'hi-IN-Wavenet-B',
        },
    }

    # Cost per character in USD
    COST_PER_CHAR_STANDARD = 4.0 / 1_000_000  # $4 per million
    COST_PER_CHAR_WAVENET = 16.0 / 1_000_000  # $16 per million

    @classmethod
    def _create_simple_ssml(cls, text: str) -> str:
        """
        Create simple, clear SSML for short text like vocabulary and grammar examples.
        Uses child-friendly settings with natural pitch and comfortable pace.

        Settings optimized for kids:
        - rate="95%": Slightly slower for clarity, but not too slow
        - pitch="+2st": Slightly higher pitch (more engaging for kids, less robotic)
        """
        # Child-friendly pronunciation - natural pace with slightly higher pitch
        return f'<speak><prosody rate="95%" pitch="+2st">{text}</prosody></speak>'

    @classmethod
    def _create_storytelling_ssml(cls, text: str) -> str:
        """
        Convert plain text to expressive SSML for child-friendly storytelling.
        Adds voice modulations, pauses, and emphasis to keep kids engaged.

        NOTE: Only used for longer story content. Short text uses _create_simple_ssml.
        """
        import re

        # For short text (< 100 chars), use simple clear pronunciation
        if len(text) < 100:
            return cls._create_simple_ssml(text)

        # Split into sentences for individual treatment
        sentences = re.split(r'([।\.\!\?]+)', text)

        ssml_parts = ['<speak>']

        for i, part in enumerate(sentences):
            part = part.strip()
            if not part:
                continue

            # Check if this is punctuation
            if re.match(r'^[।\.\!\?]+$', part):
                # Add appropriate pause after punctuation
                if '!' in part or '?' in part:
                    ssml_parts.append('<break time="600ms"/>')
                else:
                    ssml_parts.append('<break time="400ms"/>')
                continue

            # Add variation based on sentence position
            sentence_num = i // 2  # Every other element is a sentence

            # Alternate between different prosody styles for variety
            if sentence_num % 4 == 0:
                # Normal, warm tone
                ssml_parts.append(f'<prosody rate="95%" pitch="+1st">{part}</prosody>')
            elif sentence_num % 4 == 1:
                # Slightly slower, lower pitch for variety
                ssml_parts.append(f'<prosody rate="90%" pitch="-0.5st">{part}</prosody>')
            elif sentence_num % 4 == 2:
                # Enthusiastic, higher pitch
                ssml_parts.append(f'<prosody rate="100%" pitch="+2st">{part}</prosody>')
            else:
                # Gentle, softer tone
                ssml_parts.append(f'<prosody rate="92%" pitch="+0.5st" volume="soft">{part}</prosody>')

        ssml_parts.append('</speak>')
        return ''.join(ssml_parts)

    @classmethod
    def _create_song_ssml(cls, text: str) -> str:
        """
        Convert song lyrics to highly expressive SSML with rich emotions.

        Emotional expression techniques:
        - Dramatic pitch contours (rising/falling within phrases)
        - Volume dynamics (crescendo/decrescendo)
        - Strategic emphasis on emotional words
        - Varied pauses for dramatic effect
        - Warm, nurturing tone for children's songs
        """
        import re

        # Split into lines (songs are line-based, not sentence-based)
        lines = re.split(r'[\n।]+', text)

        ssml_parts = ['<speak>']

        # Add a warm opening breath pause
        ssml_parts.append('<break time="300ms"/>')

        total_lines = len([l for l in lines if l.strip()])
        line_count = 0

        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            # Remove any trailing punctuation for cleaner SSML
            line = re.sub(r'[।\.\,]+$', '', line).strip()
            if not line:
                continue

            line_count += 1
            # Determine position in song for emotional arc
            position_ratio = line_count / max(total_lines, 1)

            # Split line into words for word-level expression
            words = line.split()

            # Apply emotional pattern based on verse structure
            pattern = i % 8

            if pattern == 0:
                # Opening verse - warm, welcoming, gentle rise
                # Start soft, build warmth
                ssml_parts.append('<prosody rate="70%" pitch="+1st" volume="soft">')
                ssml_parts.append(f'<emphasis level="moderate">{words[0] if words else ""}</emphasis> ')
                ssml_parts.append(' '.join(words[1:]) if len(words) > 1 else '')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="600ms"/>')

            elif pattern == 1:
                # Building anticipation - rising pitch contour
                ssml_parts.append(f'<prosody rate="72%" pitch="+2st" volume="medium">{line}</prosody>')
                ssml_parts.append('<break time="500ms"/>')

            elif pattern == 2:
                # Emotional crescendo - joyful, expressive peak
                # Use pitch contour for melodic feel
                ssml_parts.append('<prosody rate="75%" volume="loud">')
                ssml_parts.append(f'<prosody pitch="+4st">{" ".join(words[:len(words)//2]) if words else ""}</prosody>')
                ssml_parts.append(' ')
                ssml_parts.append(f'<prosody pitch="+5st"><emphasis level="strong">{" ".join(words[len(words)//2:]) if words else ""}</emphasis></prosody>')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="700ms"/>')

            elif pattern == 3:
                # Tender moment - soft, loving, gentle
                ssml_parts.append('<prosody rate="68%" pitch="+1.5st" volume="soft">')
                ssml_parts.append(f'<emphasis level="reduced">{line}</emphasis>')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="800ms"/>')

            elif pattern == 4:
                # Playful bounce - energetic but warm
                if len(words) >= 2:
                    ssml_parts.append('<prosody rate="78%" volume="medium">')
                    ssml_parts.append(f'<prosody pitch="+3st">{words[0]}</prosody> ')
                    ssml_parts.append(f'<prosody pitch="+2st">{" ".join(words[1:])}</prosody>')
                    ssml_parts.append('</prosody>')
                else:
                    ssml_parts.append(f'<prosody rate="78%" pitch="+3st" volume="medium">{line}</prosody>')
                ssml_parts.append('<break time="550ms"/>')

            elif pattern == 5:
                # Wonder/curiosity - slightly questioning, engaged
                ssml_parts.append(f'<prosody rate="72%" pitch="+3.5st" volume="medium">')
                ssml_parts.append(f'{line}')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="650ms"/>')

            elif pattern == 6:
                # Celebration - joyful climax
                ssml_parts.append('<prosody rate="75%" volume="x-loud">')
                ssml_parts.append(f'<prosody pitch="+5st"><emphasis level="strong">{line}</emphasis></prosody>')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="900ms"/>')

            else:
                # Resolution/ending - warm, gentle closure
                ssml_parts.append('<prosody rate="65%" pitch="+1st" volume="soft">')
                ssml_parts.append(f'<emphasis level="moderate">{line}</emphasis>')
                ssml_parts.append('</prosody>')
                ssml_parts.append('<break time="1000ms"/>')

        # Add a gentle closing pause
        ssml_parts.append('<break time="500ms"/>')
        ssml_parts.append('</speak>')
        return ''.join(ssml_parts)

    @classmethod
    def _get_api_key(cls) -> Optional[str]:
        """Get Google TTS API key from settings or environment."""
        return getattr(settings, 'GOOGLE_TTS_API_KEY', None) or os.environ.get('GOOGLE_TTS_API_KEY')

    @classmethod
    def _setup_credentials_from_base64(cls) -> bool:
        """Decode base64 credentials and set up for Google Cloud SDK."""
        import base64
        import tempfile

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
        """Check if Google Cloud TTS is configured."""
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
    def text_to_speech(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_profile: str = 'default',
        use_wavenet: bool = False,
    ) -> Tuple[bytes, int]:
        """
        Generate TTS audio using Google Cloud REST API.

        Args:
            text: Text to convert to speech
            language: Language code (HINDI, TAMIL, etc.)
            voice_profile: Voice style ('default', 'male', 'female')
            use_wavenet: Use WaveNet voices (higher quality, PREMIUM only)

        Returns:
            Tuple of (audio_bytes, duration_ms)

        Raises:
            GoogleTTSError: If generation fails
        """
        api_key = cls._get_api_key()

        if api_key:
            return cls._generate_with_api_key(text, language, voice_profile, use_wavenet, api_key)
        else:
            return cls._generate_with_sdk(text, language, voice_profile, use_wavenet)

    @classmethod
    def _generate_with_api_key(
        cls,
        text: str,
        language: str,
        voice_profile: str,
        use_wavenet: bool,
        api_key: str,
    ) -> Tuple[bytes, int]:
        """Generate audio using REST API with API key."""
        voice_config = cls.VOICE_MAPPING.get(language, cls.VOICE_MAPPING['HINDI'])
        start_time = time.time()

        # Select voice based on profile and quality tier
        if use_wavenet and voice_config.get('wavenet_voice'):
            if voice_profile == 'male' and voice_config.get('wavenet_voice_male'):
                voice_name = voice_config['wavenet_voice_male']
            else:
                voice_name = voice_config['wavenet_voice']
        else:
            if voice_profile == 'male':
                voice_name = voice_config.get('voice_name_male', voice_config['voice_name'])
            else:
                voice_name = voice_config['voice_name']

        # Build request payload with expressive SSML
        # Use song SSML for slower, more melodic delivery; storytelling for stories
        if voice_profile == 'song':
            ssml_text = cls._create_song_ssml(text)
            # Songs need slower base rate for children to follow along
            base_speaking_rate = 0.85
        else:
            ssml_text = cls._create_storytelling_ssml(text)
            base_speaking_rate = 1.0

        payload = {
            "input": {"ssml": ssml_text},
            "voice": {
                "languageCode": voice_config['language_code'],
                "name": voice_name,
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": base_speaking_rate,  # Slower for songs, normal for stories
                "pitch": 1.5,  # Slightly higher base pitch for kid-friendly voice
                "sampleRateHertz": 24000,
                "effectsProfileId": ["headphone-class-device"],  # High quality output
            }
        }

        try:
            logger.info(f"Google TTS (API Key): Generating '{text[:30]}...' in {language} with {voice_name}")

            response = requests.post(
                f"{cls.API_URL}?key={api_key}",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30,
            )

            if response.status_code != 200:
                error_msg = response.json().get('error', {}).get('message', response.text)
                logger.error(f"Google TTS API error: {response.status_code} - {error_msg}")
                raise GoogleTTSError(f"Google TTS API error: {error_msg}")

            result = response.json()
            audio_content_b64 = result.get('audioContent')

            if not audio_content_b64:
                raise GoogleTTSError("No audio content in response")

            audio_bytes = base64.b64decode(audio_content_b64)
            generation_time_ms = int((time.time() - start_time) * 1000)

            # Estimate duration (MP3 at ~24kbps = ~3KB per second)
            duration_ms = int((len(audio_bytes) / 3000) * 1000)

            logger.info(
                f"Google TTS: Generated {len(audio_bytes)} bytes, "
                f"~{duration_ms}ms audio in {generation_time_ms}ms"
            )

            return audio_bytes, duration_ms

        except requests.RequestException as e:
            logger.error(f"Google TTS request error: {e}")
            raise GoogleTTSError(f"Network error: {e}")

    @classmethod
    def _generate_with_sdk(
        cls,
        text: str,
        language: str,
        voice_profile: str,
        use_wavenet: bool,
    ) -> Tuple[bytes, int]:
        """Generate audio using Google Cloud SDK with service account."""
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
            logger.info(f"Google TTS (SDK): Generating audio for '{text[:50]}...' in {language}")

            client = texttospeech.TextToSpeechClient()

            # Select voice
            if use_wavenet and voice_config.get('wavenet_voice'):
                if voice_profile == 'male' and voice_config.get('wavenet_voice_male'):
                    voice_name = voice_config['wavenet_voice_male']
                else:
                    voice_name = voice_config['wavenet_voice']
            else:
                if voice_profile == 'male':
                    voice_name = voice_config.get('voice_name_male', voice_config['voice_name'])
                else:
                    voice_name = voice_config['voice_name']

            voice = texttospeech.VoiceSelectionParams(
                language_code=voice_config['language_code'],
                name=voice_name,
            )

            # Use appropriate SSML based on voice profile
            # Songs get slower, more melodic delivery; stories get expressive storytelling
            if voice_profile == 'song':
                ssml_text = cls._create_song_ssml(text)
                base_speaking_rate = 0.85  # Slower for songs
            else:
                ssml_text = cls._create_storytelling_ssml(text)
                base_speaking_rate = 1.0  # Natural speed for stories

            synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=base_speaking_rate,  # Slower for songs, natural for stories
                pitch=1.5,  # Slightly higher base pitch for kid-friendly voice
                sample_rate_hertz=24000,
                effects_profile_id=['headphone-class-device'],  # High quality output
            )

            response = client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config,
            )

            audio_bytes = response.audio_content
            generation_time_ms = int((time.time() - start_time) * 1000)
            duration_ms = int((len(audio_bytes) / 3000) * 1000)

            logger.info(
                f"Google TTS: Generated {len(audio_bytes)} bytes, "
                f"~{duration_ms}ms audio in {generation_time_ms}ms"
            )

            return audio_bytes, duration_ms

        except Exception as e:
            logger.error(f"Google TTS SDK error: {e}")
            raise GoogleTTSError(str(e))

    # Alias for backward compatibility
    generate = text_to_speech

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported languages."""
        return list(cls.VOICE_MAPPING.keys())

    @classmethod
    def estimate_cost(cls, text: str, use_wavenet: bool = False) -> float:
        """Estimate cost for generating audio in USD."""
        cost_per_char = cls.COST_PER_CHAR_WAVENET if use_wavenet else cls.COST_PER_CHAR_STANDARD
        return len(text) * cost_per_char

    @classmethod
    def get_provider_name(cls) -> str:
        return "google"

    @classmethod
    def list_available_voices(cls, language: str = 'HINDI') -> dict:
        """List available voices for a language."""
        voice_config = cls.VOICE_MAPPING.get(language, cls.VOICE_MAPPING['HINDI'])
        return {
            'standard_female': voice_config['voice_name'],
            'standard_male': voice_config.get('voice_name_male'),
            'wavenet_female': voice_config.get('wavenet_voice'),
            'wavenet_male': voice_config.get('wavenet_voice_male'),
        }
