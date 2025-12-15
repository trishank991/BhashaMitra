"""
Audio caching service for TTS.
Implements a two-tier cache:
1. Redis (fast, short-term) - 24 hour TTL
2. S3/R2 (permanent, long-term) - Forever

Strategy: Generate once, cache forever, serve unlimited users.
"""
import hashlib
import logging
from typing import Optional, Tuple
from django.conf import settings
from django.core.cache import cache
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import F

from apps.speech.models import AudioCache

logger = logging.getLogger(__name__)


class AudioCacheService:
    """
    Two-tier caching for TTS audio:
    - Tier 1: Redis (fast, 24h TTL)
    - Tier 2: S3/R2 storage (permanent)
    - Tier 3: Database record (metadata + URL)
    """

    REDIS_TTL = getattr(settings, 'TTS_CACHE_TTL', 86400)  # 24 hours default
    STORAGE_PATH_PREFIX = "audio/tts"

    @classmethod
    def _generate_cache_key(cls, text: str, language: str, voice_style: str) -> str:
        """Generate a unique cache key for the text."""
        content = f"{text}:{language}:{voice_style}"
        return hashlib.md5(content.encode()).hexdigest()

    @classmethod
    def _generate_text_hash(cls, text: str) -> str:
        """Generate hash of just the text content."""
        return hashlib.md5(text.encode()).hexdigest()

    @classmethod
    def get_cached_audio(
        cls,
        text: str,
        language: str,
        voice_style: str = 'storyteller'
    ) -> Tuple[Optional[bytes], bool, Optional[str]]:
        """
        Try to get audio from cache.

        Returns:
            Tuple of (audio_bytes, was_cached, audio_url)
            - audio_bytes: The audio data if found, None otherwise
            - was_cached: True if found in any cache tier
            - audio_url: URL to the cached audio (for streaming)
        """
        cache_key = cls._generate_cache_key(text, language, voice_style)

        # Tier 1: Check Redis cache (fastest)
        redis_key = f"tts:audio:{cache_key}"
        cached_audio = cache.get(redis_key)
        if cached_audio:
            logger.debug(f"Redis cache hit for {cache_key[:8]}...")
            # Update access count in background
            cls._update_access_count(cache_key)
            return cached_audio, True, None

        # Tier 2: Check database for URL (serves from S3/R2)
        try:
            audio_cache = AudioCache.objects.get(cache_key=cache_key)

            # Try to get from storage
            storage_path = f"{cls.STORAGE_PATH_PREFIX}/{cache_key}.wav"
            if default_storage.exists(storage_path):
                # Read from storage
                with default_storage.open(storage_path, 'rb') as f:
                    audio_bytes = f.read()

                # Warm Redis cache for next request
                cache.set(redis_key, audio_bytes, cls.REDIS_TTL)

                # Update access count
                audio_cache.increment_access()

                logger.debug(f"Storage cache hit for {cache_key[:8]}...")
                return audio_bytes, True, audio_cache.audio_url

        except AudioCache.DoesNotExist:
            pass
        except Exception as e:
            logger.warning(f"Cache lookup error: {e}")

        logger.debug(f"Cache miss for {cache_key[:8]}...")
        return None, False, None

    @classmethod
    def store_audio(
        cls,
        text: str,
        language: str,
        voice_style: str,
        audio_bytes: bytes,
        generation_time_ms: int = 0,
        story_id: Optional[str] = None,
        page_number: Optional[int] = None
    ) -> AudioCache:
        """
        Store generated audio in all cache tiers.

        Args:
            text: Original text
            language: Language code
            voice_style: Voice style used
            audio_bytes: Generated audio data
            generation_time_ms: Time taken to generate
            story_id: Optional story ID (for pre-warming)
            page_number: Optional page number

        Returns:
            AudioCache model instance
        """
        cache_key = cls._generate_cache_key(text, language, voice_style)
        text_hash = cls._generate_text_hash(text)

        # Tier 1: Store in Redis
        redis_key = f"tts:audio:{cache_key}"
        cache.set(redis_key, audio_bytes, cls.REDIS_TTL)

        # Tier 2: Store in S3/R2 (or local storage)
        storage_path = f"{cls.STORAGE_PATH_PREFIX}/{cache_key}.wav"
        try:
            saved_path = default_storage.save(storage_path, ContentFile(audio_bytes))
            audio_url = default_storage.url(saved_path)
        except Exception as e:
            logger.warning(f"Failed to save to storage: {e}")
            audio_url = ""

        # Calculate estimated cost (~$0.00012/second, assume 3 seconds)
        estimated_cost = 0.00036  # ~3 seconds of GPU time

        # Tier 3: Store metadata in database
        audio_cache, created = AudioCache.objects.update_or_create(
            cache_key=cache_key,
            defaults={
                'text_content': text,
                'text_hash': text_hash,
                'language': language,
                'voice_style': voice_style,
                'audio_url': audio_url,
                'audio_size_bytes': len(audio_bytes),
                'audio_format': 'wav',
                'generation_time_ms': generation_time_ms,
                'generation_cost_usd': estimated_cost,
                'story_id': story_id,
                'page_number': page_number,
            }
        )

        logger.info(
            f"Cached audio: {cache_key[:8]}... "
            f"({len(audio_bytes)} bytes, {generation_time_ms}ms)"
        )

        return audio_cache

    @classmethod
    def _update_access_count(cls, cache_key: str):
        """Update access count in background."""
        try:
            AudioCache.objects.filter(cache_key=cache_key).update(
                access_count=F('access_count') + 1
            )
        except Exception as e:
            logger.warning(f"Failed to update access count: {e}")

    @classmethod
    def get_cache_stats(cls) -> dict:
        """Get cache statistics for monitoring."""
        from django.db.models import Sum, Count, Avg

        stats = AudioCache.objects.aggregate(
            total_entries=Count('id'),
            total_size_bytes=Sum('audio_size_bytes'),
            total_cost_usd=Sum('generation_cost_usd'),
            total_accesses=Sum('access_count'),
            avg_generation_time=Avg('generation_time_ms'),
        )

        # Calculate savings
        if stats['total_accesses'] and stats['total_entries']:
            cache_hits = stats['total_accesses'] - stats['total_entries']
            savings = cache_hits * 0.00036  # Cost per generation avoided
            stats['estimated_savings_usd'] = round(savings, 4)
        else:
            stats['estimated_savings_usd'] = 0

        return stats

    @classmethod
    def get_story_page_audio_url(cls, story_id: str, page_number: int) -> Optional[str]:
        """
        Get the audio URL for a specific story page.
        Useful for pre-loading audio in the frontend.
        """
        try:
            audio_cache = AudioCache.objects.get(
                story_id=story_id,
                page_number=page_number
            )
            return audio_cache.audio_url
        except AudioCache.DoesNotExist:
            return None
