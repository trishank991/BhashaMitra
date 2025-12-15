"""
BhashaMitra TTS Service
Tier-based architecture with subscription-aware provider routing.

Tier Strategy (Updated Dec 2024):
- FREE ($0): Svara TTS for all content (alphabet, vocabulary, stories)
- STANDARD ($12/month): Svara TTS for all content
- PREMIUM ($20/month): Sarvam AI Bulbul V2 (manisha/abhilash human-like voices)

Fallback chain:
1. Cache (instant, free)
2. Sarvam AI (Premium tier only)
3. Svara TTS (FREE/Standard tier, or Premium fallback)

Feature restrictions by tier:
- Stories: FREE=4, STANDARD=8, PREMIUM=unlimited
- Games/Quizzes: STANDARD and PREMIUM only
- Cultural Videos: STANDARD and PREMIUM only
"""
import hashlib
import logging
import time
from typing import Tuple, Optional, TYPE_CHECKING
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.conf import settings

from apps.speech.models import AudioCache, TTSUsageLog

if TYPE_CHECKING:
    from apps.users.models import User

logger = logging.getLogger(__name__)


class TTSServiceError(Exception):
    """TTS Service error."""
    pass


class TTSService:
    """
    Hybrid TTS Service with three-tier fallback.

    Priority:
    1. Local cache (instant, free) - 80% of requests
    2. Replicate.com (fast, cheap) - dynamic content
    3. Google Cloud TTS (reliable) - fallback
    4. Svara TTS (legacy) - last resort if others fail

    NO BHASHINI - works internationally without Indian registration.
    """

    # Redis cache TTL (30 days)
    REDIS_CACHE_TTL = 86400 * 30

    # Maximum text length
    MAX_TEXT_LENGTH = 5000

    @classmethod
    def _generate_cache_key(cls, text: str, language: str, voice_profile: str) -> str:
        """Generate unique cache key for audio."""
        content = f"{text}:{language}:{voice_profile}"
        return hashlib.md5(content.encode()).hexdigest()

    @classmethod
    def _generate_text_hash(cls, text: str) -> str:
        """Generate hash of text content."""
        return hashlib.md5(text.encode()).hexdigest()

    @classmethod
    def get_audio(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_profile: str = 'default',
        force_regenerate: bool = False,
        user: Optional['User'] = None,
    ) -> Tuple[bytes, str, bool]:
        """
        Get audio for text using tier-based provider routing.

        Args:
            text: Text to convert to speech
            language: Language code (HINDI, TAMIL, etc.)
            voice_profile: Voice style
            force_regenerate: Skip cache and regenerate
            user: User object to determine subscription tier

        Provider Routing:
            - FREE tier: Cache only (raises error if not cached)
            - STANDARD tier: Cache → Svara TTS
            - PREMIUM tier: Cache → Sarvam AI → Svara TTS (fallback)

        Returns:
            Tuple of (audio_bytes, provider_name, was_cached)

        Raises:
            TTSServiceError: If provider fails or content not available for tier
        """
        start_time = time.time()

        # Validate input
        if not text or not text.strip():
            raise TTSServiceError("Text cannot be empty")

        text = text.strip()
        if len(text) > cls.MAX_TEXT_LENGTH:
            raise TTSServiceError(f"Text too long (max {cls.MAX_TEXT_LENGTH} characters)")

        cache_key = cls._generate_cache_key(text, language, voice_profile)

        # Determine user's tier (default to FREE if no user)
        user_tier = 'cache_only'
        if user:
            user_tier = user.tts_provider

        # Step 1: Always check cache first (all tiers benefit from cache)
        if not force_regenerate:
            cached_audio = cls._get_from_cache(cache_key)
            if cached_audio:
                cls._log_usage(
                    text_length=len(text),
                    language=language,
                    provider='cache',
                    voice_profile=voice_profile,
                    was_cached=True,
                    response_time_ms=int((time.time() - start_time) * 1000),
                )
                return cached_audio, 'cache', True

        # FREE tier: Cache only - reject if not cached
        if user_tier == 'cache_only':
            cls._log_usage(
                text_length=len(text),
                language=language,
                provider='none',
                voice_profile=voice_profile,
                was_cached=False,
                response_time_ms=int((time.time() - start_time) * 1000),
                success=False,
                error_message="Content not available for free tier",
            )
            raise TTSServiceError(
                "This audio is not available for free users. "
                "Upgrade to Standard ($12/month) for unlimited content."
            )

        # PREMIUM tier: Try Sarvam AI first
        if user_tier == 'sarvam':
            try:
                from apps.speech.services.sarvam_provider import SarvamAIProvider

                if SarvamAIProvider.is_available():
                    try:
                        audio_bytes, duration_ms = SarvamAIProvider.text_to_speech(
                            text=text,
                            language=language,
                        )
                        cls._save_to_cache(
                            cache_key=cache_key,
                            text=text,
                            language=language,
                            voice_profile=voice_profile,
                            audio_bytes=audio_bytes,
                            duration_ms=duration_ms,
                            provider='sarvam',
                        )
                        cls._log_usage(
                            text_length=len(text),
                            language=language,
                            provider='sarvam',
                            voice_profile=voice_profile,
                            was_cached=False,
                            response_time_ms=int((time.time() - start_time) * 1000),
                            estimated_cost=SarvamAIProvider.estimate_cost(text),
                        )
                        return audio_bytes, 'sarvam', False
                    except Exception as e:
                        logger.warning(f"Sarvam AI TTS failed, falling back to Svara: {e}")
            except ImportError:
                logger.warning("Sarvam provider not available, falling back to Svara")

        # STANDARD tier (or PREMIUM fallback): Use Svara TTS
        if user_tier in ['svara', 'sarvam']:
            try:
                from apps.speech.services.mms_provider import SvaraTTSProvider

                if SvaraTTSProvider.is_available():
                    try:
                        audio_bytes, duration_ms = SvaraTTSProvider.text_to_speech(
                            text=text,
                            language=language,
                        )
                        cls._save_to_cache(
                            cache_key=cache_key,
                            text=text,
                            language=language,
                            voice_profile=voice_profile,
                            audio_bytes=audio_bytes,
                            duration_ms=duration_ms,
                            provider='svara',
                        )
                        cls._log_usage(
                            text_length=len(text),
                            language=language,
                            provider='svara',
                            voice_profile=voice_profile,
                            was_cached=False,
                            response_time_ms=int((time.time() - start_time) * 1000),
                        )
                        return audio_bytes, 'svara', False
                    except Exception as e:
                        logger.error(f"Svara TTS failed: {e}")
            except ImportError:
                logger.error("Svara provider not available")

        # All providers failed
        cls._log_usage(
            text_length=len(text),
            language=language,
            provider='none',
            voice_profile=voice_profile,
            was_cached=False,
            response_time_ms=int((time.time() - start_time) * 1000),
            success=False,
            error_message="All TTS providers failed",
        )
        raise TTSServiceError("TTS service temporarily unavailable. Please try again later.")

    @classmethod
    def _get_from_cache(cls, cache_key: str) -> Optional[bytes]:
        """
        Get audio from cache (Redis first, then database).
        """
        # Check Redis cache first (fastest)
        redis_key = f"tts:audio:{cache_key}"
        cached = cache.get(redis_key)
        if cached:
            logger.debug(f"TTS cache hit (Redis): {cache_key}")
            return cached

        # Check database
        try:
            audio_cache = AudioCache.objects.get(cache_key=cache_key)

            # Read audio from file
            if audio_cache.audio_file:
                audio_cache.audio_file.open('rb')
                audio_bytes = audio_cache.audio_file.read()
                audio_cache.audio_file.close()
            else:
                return None

            # Repopulate Redis cache
            cache.set(redis_key, audio_bytes, cls.REDIS_CACHE_TTL)

            # Update access count
            audio_cache.increment_access()

            logger.debug(f"TTS cache hit (DB): {cache_key}")
            return audio_bytes

        except AudioCache.DoesNotExist:
            return None
        except Exception as e:
            logger.warning(f"Error reading from cache: {e}")
            return None

    @classmethod
    def _save_to_cache(
        cls,
        cache_key: str,
        text: str,
        language: str,
        voice_profile: str,
        audio_bytes: bytes,
        duration_ms: int,
        provider: str,
    ):
        """
        Save audio to both Redis and database.
        """
        # Save to Redis
        redis_key = f"tts:audio:{cache_key}"
        cache.set(redis_key, audio_bytes, cls.REDIS_CACHE_TTL)

        # Save to database
        try:
            audio_cache, created = AudioCache.objects.update_or_create(
                cache_key=cache_key,
                defaults={
                    'text_hash': cls._generate_text_hash(text),
                    'text_content': text,
                    'language': language,
                    'voice_style': voice_profile,
                    'provider': provider,
                    'audio_size_bytes': len(audio_bytes),
                    'audio_duration_ms': duration_ms,
                }
            )

            # Save audio file
            audio_cache.audio_file.save(
                f"{cache_key}.wav",
                ContentFile(audio_bytes),
                save=True,
            )

            logger.info(f"TTS cached: {cache_key} ({provider}, {len(audio_bytes)} bytes)")
        except Exception as e:
            logger.error(f"Failed to save to database cache: {e}")

    @classmethod
    def _log_usage(
        cls,
        text_length: int,
        language: str,
        provider: str,
        voice_profile: str,
        was_cached: bool,
        response_time_ms: int,
        success: bool = True,
        error_message: str = '',
        estimated_cost: float = 0,
    ):
        """Log TTS usage for monitoring."""
        try:
            TTSUsageLog.objects.create(
                text_length=text_length,
                language=language,
                provider=provider,
                voice_style=voice_profile,
                was_cached=was_cached,
                response_time_ms=response_time_ms,
                success=success,
                error_message=error_message,
                estimated_cost_cents=estimated_cost * 100,  # Convert to cents
            )
        except Exception as e:
            logger.error(f"Failed to log TTS usage: {e}")

    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported languages."""
        # Combined from all providers
        return [
            'HINDI', 'TAMIL', 'TELUGU', 'GUJARATI', 'PUNJABI',
            'MALAYALAM', 'BENGALI', 'KANNADA', 'MARATHI'
        ]

    @classmethod
    def get_cache_stats(cls) -> dict:
        """Get cache statistics."""
        from django.db.models import Sum, Count

        stats = AudioCache.objects.aggregate(
            total_cached=Count('id'),
            total_size_bytes=Sum('audio_size_bytes'),
            total_accesses=Sum('access_count'),
        )

        # Get usage by provider
        provider_stats = TTSUsageLog.objects.values('provider').annotate(
            count=Count('id'),
            total_cost=Sum('estimated_cost_cents'),
        )

        return {
            'cache': {
                'total_entries': stats['total_cached'] or 0,
                'total_size_mb': (stats['total_size_bytes'] or 0) / (1024 * 1024),
                'total_accesses': stats['total_accesses'] or 0,
            },
            'usage_by_provider': {
                item['provider']: {
                    'count': item['count'],
                    'cost_usd': (item['total_cost'] or 0) / 100,
                }
                for item in provider_stats
            },
        }

    # Legacy compatibility methods
    @classmethod
    def text_to_speech(
        cls,
        text: str,
        language: str = 'HINDI',
        voice_style: str = 'default',
        user_id: Optional[str] = None,
        user: Optional['User'] = None,
        story_id: Optional[str] = None,
        page_number: Optional[int] = None,
    ) -> Tuple[bytes, bool]:
        """
        Legacy method for backward compatibility.

        Args:
            text: Text to convert to speech
            language: Language code
            voice_style: Voice style
            user_id: User ID (used to lookup user if user not provided)
            user: User object for tier-based routing
            story_id: Story ID (for logging)
            page_number: Page number (for logging)

        Returns:
            Tuple of (audio_bytes, was_cached)
        """
        # If user_id provided but no user object, look up the user
        if user_id and not user:
            try:
                from apps.users.models import User as UserModel
                user = UserModel.objects.get(id=user_id)
            except Exception:
                pass  # User not found, will use free tier

        audio_bytes, provider, was_cached = cls.get_audio(
            text=text,
            language=language,
            voice_profile=voice_style,
            user=user,
        )
        return audio_bytes, was_cached

    @classmethod
    def check_service_status(cls) -> dict:
        """Check if the TTS service is healthy."""
        providers = []

        # Check Sarvam AI (Premium tier)
        try:
            from apps.speech.services.sarvam_provider import SarvamAIProvider
            providers.append({
                'name': 'sarvam',
                'available': SarvamAIProvider.is_available(),
                'tier': 'premium',
                'description': 'Sarvam AI Bulbul V2 - Human-like voices',
            })
        except ImportError:
            pass

        # Check Svara TTS (Standard tier)
        try:
            from apps.speech.services.mms_provider import SvaraTTSProvider
            providers.append({
                'name': 'svara',
                'available': SvaraTTSProvider.is_available(),
                'tier': 'standard',
                'description': 'Svara TTS - AI-generated voices',
            })
        except ImportError:
            pass

        has_available = any(p['available'] for p in providers)

        return {
            'status': 'healthy' if has_available else 'degraded',
            'providers': providers,
            'supported_languages': cls.get_supported_languages(),
            'cache_stats': cls.get_cache_stats(),
            'tier_info': {
                'free': {'provider': 'cache_only', 'description': 'Pre-cached content only'},
                'standard': {'provider': 'svara', 'price': 'NZD $12/month', 'description': 'Unlimited Svara TTS'},
                'premium': {'provider': 'sarvam', 'price': 'NZD $20/month', 'description': 'Sarvam AI human-like voices'},
            }
        }
