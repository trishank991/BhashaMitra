"""
Centralized Caching Service for BhashaMitra.

Caching Strategy:
=================

1. STATIC CURRICULUM CONTENT (24h TTL) - Redis + Browser:
   - Scripts/Letters: Rarely changes, safe to cache long
   - Vocabulary Themes/Words: Stable content
   - Grammar Topics/Rules: Stable content
   - Stories: Content doesn't change once published
   - Games: Game definitions are static

2. USER PROGRESS (5-15 min TTL) - Redis only:
   - Child progress: Updates frequently during sessions
   - SRS word progress: Critical for learning, short cache
   - Game history: Recent activity

3. HOMEPAGE DATA (1-5 min TTL) - Redis:
   - Curriculum stats: Aggregated counts
   - Streak/XP: Frequently updated

4. API RESPONSE CACHING:
   - Use @cache_response decorator for expensive queries
   - Automatic cache invalidation on data changes

Cache Key Patterns:
==================
- curriculum:{lang}:scripts          - All scripts for language
- curriculum:{lang}:vocab:themes     - Vocabulary themes
- curriculum:{lang}:vocab:{theme_id} - Words for a theme
- curriculum:{lang}:grammar:topics   - Grammar topics
- curriculum:{lang}:stories          - Stories list
- curriculum:{lang}:games            - Games list
- progress:{child_id}:summary        - Child progress summary
- progress:{child_id}:srs            - SRS due words
- homepage:{child_id}:stats          - Homepage statistics
"""

import hashlib
import logging
from typing import Any, Optional, Callable
from functools import wraps
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class CacheConfig:
    """Cache TTL configuration (in seconds)."""

    # Static curriculum content - cache for 24 hours
    CURRICULUM_TTL = 86400  # 24 hours

    # User progress - cache for 5 minutes
    PROGRESS_TTL = 300  # 5 minutes

    # Homepage stats - cache for 1 minute
    HOMEPAGE_TTL = 60  # 1 minute

    # SRS due words - cache for 2 minutes (needs to be fresh)
    SRS_TTL = 120  # 2 minutes

    # Game sessions - cache for 10 minutes
    GAME_TTL = 600  # 10 minutes


class CurriculumCacheService:
    """Cache service for curriculum content."""

    @classmethod
    def _make_key(cls, *parts: str) -> str:
        """Generate cache key from parts."""
        return ":".join(["curriculum"] + list(parts))

    @classmethod
    def get_scripts(cls, language: str) -> Optional[list]:
        """Get cached scripts for a language."""
        key = cls._make_key(language, "scripts")
        return cache.get(key)

    @classmethod
    def set_scripts(cls, language: str, scripts: list) -> None:
        """Cache scripts for a language."""
        key = cls._make_key(language, "scripts")
        cache.set(key, scripts, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached scripts for {language}")

    @classmethod
    def get_vocab_themes(cls, language: str) -> Optional[list]:
        """Get cached vocabulary themes."""
        key = cls._make_key(language, "vocab", "themes")
        return cache.get(key)

    @classmethod
    def set_vocab_themes(cls, language: str, themes: list) -> None:
        """Cache vocabulary themes."""
        key = cls._make_key(language, "vocab", "themes")
        cache.set(key, themes, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached {len(themes)} vocab themes for {language}")

    @classmethod
    def get_vocab_words(cls, theme_id: str) -> Optional[list]:
        """Get cached vocabulary words for a theme."""
        key = cls._make_key("vocab", "words", theme_id)
        return cache.get(key)

    @classmethod
    def set_vocab_words(cls, theme_id: str, words: list) -> None:
        """Cache vocabulary words for a theme."""
        key = cls._make_key("vocab", "words", theme_id)
        cache.set(key, words, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached {len(words)} words for theme {theme_id}")

    @classmethod
    def get_grammar_topics(cls, language: str) -> Optional[list]:
        """Get cached grammar topics."""
        key = cls._make_key(language, "grammar", "topics")
        return cache.get(key)

    @classmethod
    def set_grammar_topics(cls, language: str, topics: list) -> None:
        """Cache grammar topics."""
        key = cls._make_key(language, "grammar", "topics")
        cache.set(key, topics, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached {len(topics)} grammar topics for {language}")

    @classmethod
    def get_stories(cls, language: str) -> Optional[list]:
        """Get cached stories."""
        key = cls._make_key(language, "stories")
        return cache.get(key)

    @classmethod
    def set_stories(cls, language: str, stories: list) -> None:
        """Cache stories."""
        key = cls._make_key(language, "stories")
        cache.set(key, stories, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached {len(stories)} stories for {language}")

    @classmethod
    def get_games(cls, language: str) -> Optional[list]:
        """Get cached games."""
        key = cls._make_key(language, "games")
        return cache.get(key)

    @classmethod
    def set_games(cls, language: str, games: list) -> None:
        """Cache games."""
        key = cls._make_key(language, "games")
        cache.set(key, games, CacheConfig.CURRICULUM_TTL)
        logger.debug(f"Cached {len(games)} games for {language}")

    @classmethod
    def invalidate_language(cls, language: str) -> None:
        """Invalidate all curriculum cache for a language."""
        keys = [
            cls._make_key(language, "scripts"),
            cls._make_key(language, "vocab", "themes"),
            cls._make_key(language, "grammar", "topics"),
            cls._make_key(language, "stories"),
            cls._make_key(language, "games"),
        ]
        cache.delete_many(keys)
        logger.info(f"Invalidated curriculum cache for {language}")


class ProgressCacheService:
    """Cache service for user progress data."""

    @classmethod
    def _make_key(cls, *parts: str) -> str:
        """Generate cache key from parts."""
        return ":".join(["progress"] + list(parts))

    @classmethod
    def get_child_summary(cls, child_id: str) -> Optional[dict]:
        """Get cached progress summary for a child."""
        key = cls._make_key(child_id, "summary")
        return cache.get(key)

    @classmethod
    def set_child_summary(cls, child_id: str, summary: dict) -> None:
        """Cache progress summary for a child."""
        key = cls._make_key(child_id, "summary")
        cache.set(key, summary, CacheConfig.PROGRESS_TTL)

    @classmethod
    def get_srs_due(cls, child_id: str, theme_id: str = None) -> Optional[list]:
        """Get cached SRS due words."""
        parts = [child_id, "srs"]
        if theme_id:
            parts.append(theme_id)
        key = cls._make_key(*parts)
        return cache.get(key)

    @classmethod
    def set_srs_due(cls, child_id: str, due_words: list, theme_id: str = None) -> None:
        """Cache SRS due words."""
        parts = [child_id, "srs"]
        if theme_id:
            parts.append(theme_id)
        key = cls._make_key(*parts)
        cache.set(key, due_words, CacheConfig.SRS_TTL)

    @classmethod
    def invalidate_child_progress(cls, child_id: str) -> None:
        """Invalidate all progress cache for a child."""
        # Note: In production, use Redis KEYS pattern or maintain a key registry
        key = cls._make_key(child_id, "summary")
        cache.delete(key)
        logger.debug(f"Invalidated progress cache for child {child_id}")


class HomepageCacheService:
    """Cache service for homepage statistics."""

    @classmethod
    def _make_key(cls, child_id: str, *parts: str) -> str:
        """Generate cache key from parts."""
        return ":".join(["homepage", child_id] + list(parts))

    @classmethod
    def get_stats(cls, child_id: str, language: str) -> Optional[dict]:
        """Get cached homepage stats."""
        key = cls._make_key(child_id, language, "stats")
        return cache.get(key)

    @classmethod
    def set_stats(cls, child_id: str, language: str, stats: dict) -> None:
        """Cache homepage stats."""
        key = cls._make_key(child_id, language, "stats")
        cache.set(key, stats, CacheConfig.HOMEPAGE_TTL)

    @classmethod
    def invalidate_child(cls, child_id: str) -> None:
        """Invalidate homepage cache for a child."""
        # Will be re-fetched on next request
        pass


def cache_response(ttl: int = 300, key_prefix: str = "api"):
    """
    Decorator to cache API response.

    Usage:
        @cache_response(ttl=300, key_prefix="scripts")
        def get(self, request, child_id):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Build cache key from request
            cache_key_parts = [
                key_prefix,
                request.path,
                str(args),
                str(sorted(request.query_params.items())),
            ]
            cache_key = hashlib.md5(
                ":".join(cache_key_parts).encode()
            ).hexdigest()

            # Check cache
            cached = cache.get(cache_key)
            if cached is not None:
                logger.debug(f"Cache hit: {key_prefix}")
                return cached

            # Execute function
            response = func(self, request, *args, **kwargs)

            # Cache successful responses
            if hasattr(response, 'status_code') and response.status_code == 200:
                cache.set(cache_key, response, ttl)
                logger.debug(f"Cached: {key_prefix}")

            return response
        return wrapper
    return decorator


# Utility functions for cache warming

def warm_curriculum_cache(language: str) -> dict:
    """
    Pre-warm curriculum cache for a language.
    Returns stats about cached items.
    """
    from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord
    from apps.curriculum.models.grammar import GrammarTopic
    from apps.curriculum.models.script import Script
    from apps.stories.models import Story
    from apps.curriculum.models.games import Game

    stats = {
        'language': language,
        'scripts': 0,
        'vocab_themes': 0,
        'grammar_topics': 0,
        'stories': 0,
        'games': 0,
    }

    # Cache scripts (Script model doesn't have is_active field)
    scripts = list(Script.objects.filter(language=language).values())
    if scripts:
        CurriculumCacheService.set_scripts(language, scripts)
        stats['scripts'] = len(scripts)

    # Cache vocabulary themes
    themes = list(VocabularyTheme.objects.filter(
        language=language, is_active=True
    ).values())
    if themes:
        CurriculumCacheService.set_vocab_themes(language, themes)
        stats['vocab_themes'] = len(themes)

    # Cache grammar topics
    topics = list(GrammarTopic.objects.filter(
        language=language, is_active=True
    ).values())
    if topics:
        CurriculumCacheService.set_grammar_topics(language, topics)
        stats['grammar_topics'] = len(topics)

    # Cache stories (Story model uses is_active instead of is_published)
    stories = list(Story.objects.filter(
        language=language, is_active=True
    ).values('id', 'title', 'title_hindi', 'age_min', 'age_max', 'tier'))
    if stories:
        CurriculumCacheService.set_stories(language, stories)
        stats['stories'] = len(stories)

    # Cache games
    games = list(Game.objects.filter(
        language=language, is_active=True
    ).values('id', 'name', 'game_type', 'level', 'skill_focus'))
    if games:
        CurriculumCacheService.set_games(language, games)
        stats['games'] = len(games)

    logger.info(f"Warmed curriculum cache for {language}: {stats}")
    return stats


def warm_all_curriculum_caches() -> list:
    """Pre-warm curriculum cache for all languages."""
    languages = ['HINDI', 'PUNJABI', 'TAMIL', 'TELUGU', 'GUJARATI', 'MALAYALAM']
    results = []

    for lang in languages:
        try:
            stats = warm_curriculum_cache(lang)
            results.append(stats)
        except Exception as e:
            logger.error(f"Failed to warm cache for {lang}: {e}")
            results.append({'language': lang, 'error': str(e)})

    return results
