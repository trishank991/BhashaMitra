"""
Management command to cache audio for all curriculum content across all languages.
Uses Svara TTS (free tier) to generate pronunciation audio.

Usage:
    python manage.py cache_all_audio                      # Cache all languages
    python manage.py cache_all_audio --language TAMIL     # Cache specific language
    python manage.py cache_all_audio --type letters       # Cache only letters
    python manage.py cache_all_audio --dry-run            # Show what would be cached
"""
import time
from django.core.management.base import BaseCommand
from django.db import models

from apps.speech.models import AudioCache
from apps.speech.services.tts_service import TTSService, TTSServiceError
from apps.curriculum.models import (
    Script, Letter, Matra, VocabularyWord, VocabularyTheme, PeppiPhrase
)


class Command(BaseCommand):
    help = 'Cache TTS audio for all curriculum content across all languages using Svara'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default=None,
            help='Specific language to cache (HINDI, TAMIL, PUNJABI, etc.). Default: all languages'
        )
        parser.add_argument(
            '--type',
            type=str,
            choices=['letters', 'matras', 'vocabulary', 'peppi', 'all'],
            default='all',
            help='Content type to cache (default: all)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be cached without actually generating audio'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Regenerate even if already cached'
        )
        parser.add_argument(
            '--delay',
            type=float,
            default=0.3,
            help='Delay between API calls in seconds (default: 0.3)'
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Show progress every N items (default: 50)'
        )

    def handle(self, *args, **options):
        language = options['language']
        content_type = options['type']
        dry_run = options['dry_run']
        force = options['force']
        delay = options['delay']
        batch_size = options['batch_size']

        self.stdout.write(self.style.NOTICE("=" * 60))
        self.stdout.write(self.style.NOTICE("BhashaMitra Multi-Language Audio Cache"))
        self.stdout.write(self.style.NOTICE("=" * 60))

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No audio will be generated"))

        # Get languages to process
        if language:
            languages = [language.upper()]
            self.stdout.write(f"Language: {language}")
        else:
            # Get all languages that have curriculum content
            languages = list(Script.objects.values_list('language', flat=True).distinct())
            self.stdout.write(f"Languages: {', '.join(languages)}")

        if not languages:
            self.stdout.write(self.style.ERROR("No languages found in database. Run seed commands first."))
            return

        # Track overall stats
        total_stats = {
            'total': 0,
            'cached': 0,
            'generated': 0,
            'failed': 0,
        }

        for lang in languages:
            self.stdout.write(f"\n{'=' * 40}")
            self.stdout.write(self.style.SUCCESS(f"Processing: {lang}"))
            self.stdout.write("=" * 40)

            lang_stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

            # Cache letters
            if content_type in ['letters', 'all']:
                self.stdout.write("\n>>> Caching Letters...")
                letter_stats = self._cache_letters(lang, dry_run, force, delay, batch_size)
                self._add_stats(lang_stats, letter_stats)

            # Cache matras
            if content_type in ['matras', 'all']:
                self.stdout.write("\n>>> Caching Matras...")
                matra_stats = self._cache_matras(lang, dry_run, force, delay, batch_size)
                self._add_stats(lang_stats, matra_stats)

            # Cache vocabulary
            if content_type in ['vocabulary', 'all']:
                self.stdout.write("\n>>> Caching Vocabulary...")
                vocab_stats = self._cache_vocabulary(lang, dry_run, force, delay, batch_size)
                self._add_stats(lang_stats, vocab_stats)

            # Cache Peppi phrases
            if content_type in ['peppi', 'all']:
                self.stdout.write("\n>>> Caching Peppi Phrases...")
                peppi_stats = self._cache_peppi_phrases(lang, dry_run, force, delay, batch_size)
                self._add_stats(lang_stats, peppi_stats)

            # Language summary
            self.stdout.write(f"\n{lang} Summary: "
                            f"Total={lang_stats['total']}, "
                            f"Cached={lang_stats['cached']}, "
                            f"Generated={lang_stats['generated']}, "
                            f"Failed={lang_stats['failed']}")

            self._add_stats(total_stats, lang_stats)

        # Final summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("COMPLETE!"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"Total items: {total_stats['total']}")
        self.stdout.write(f"Already cached: {total_stats['cached']}")
        self.stdout.write(f"Newly generated: {total_stats['generated']}")
        if total_stats['failed'] > 0:
            self.stdout.write(self.style.ERROR(f"Failed: {total_stats['failed']}"))
        else:
            self.stdout.write(self.style.SUCCESS("No failures!"))

    def _add_stats(self, target: dict, source: dict):
        """Add source stats to target stats."""
        for key in target:
            target[key] += source.get(key, 0)

    def _cache_letters(self, language: str, dry_run: bool, force: bool, delay: float, batch_size: int) -> dict:
        """Cache audio for all letters in a language."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        # Get letters for this language through Script -> AlphabetCategory -> Letter
        try:
            script = Script.objects.get(language=language)
        except Script.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"  No script found for {language}"))
            return stats

        letters = Letter.objects.filter(
            category__script=script,
            is_active=True
        ).select_related('category').order_by('category__order', 'order')

        self.stdout.write(f"  Found {letters.count()} letters")

        for i, letter in enumerate(letters):
            # Cache the letter character
            stats['total'] += 1
            self._generate_audio(
                text=letter.character,
                language=language,
                content_type='letter',
                content_id=f"{letter.category.category_type}_{letter.romanization}",
                dry_run=dry_run,
                force=force,
                stats=stats,
            )

            # Cache the example word if present
            if letter.example_word:
                stats['total'] += 1
                self._generate_audio(
                    text=letter.example_word,
                    language=language,
                    content_type='letter_example',
                    content_id=f"{letter.romanization}_example",
                    dry_run=dry_run,
                    force=force,
                    stats=stats,
                )

            # Progress update
            if (i + 1) % batch_size == 0:
                self.stdout.write(f"  Progress: {i + 1}/{letters.count()}")

            if not dry_run:
                time.sleep(delay)

        return stats

    def _cache_matras(self, language: str, dry_run: bool, force: bool, delay: float, batch_size: int) -> dict:
        """Cache audio for all matras in a language."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        try:
            script = Script.objects.get(language=language)
        except Script.DoesNotExist:
            return stats

        matras = Matra.objects.filter(script=script).order_by('order')
        self.stdout.write(f"  Found {matras.count()} matras")

        for i, matra in enumerate(matras):
            # Cache the matra symbol
            stats['total'] += 1
            self._generate_audio(
                text=matra.symbol,
                language=language,
                content_type='matra',
                content_id=f"matra_{matra.name}",
                dry_run=dry_run,
                force=force,
                stats=stats,
            )

            # Cache the example with consonant (e.g., का, கா)
            if matra.example_with_ka:
                stats['total'] += 1
                self._generate_audio(
                    text=matra.example_with_ka,
                    language=language,
                    content_type='matra_example',
                    content_id=f"matra_{matra.name}_example",
                    dry_run=dry_run,
                    force=force,
                    stats=stats,
                )

            if (i + 1) % batch_size == 0:
                self.stdout.write(f"  Progress: {i + 1}/{matras.count()}")

            if not dry_run:
                time.sleep(delay)

        return stats

    def _cache_vocabulary(self, language: str, dry_run: bool, force: bool, delay: float, batch_size: int) -> dict:
        """Cache audio for all vocabulary words in a language."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        themes = VocabularyTheme.objects.filter(language=language, is_active=True)
        words = VocabularyWord.objects.filter(theme__in=themes).select_related('theme').order_by('theme__order', 'order')

        self.stdout.write(f"  Found {words.count()} vocabulary words across {themes.count()} themes")

        for i, word in enumerate(words):
            stats['total'] += 1
            self._generate_audio(
                text=word.word,
                language=language,
                content_type=f'vocabulary_{word.theme.name}',
                content_id=word.romanization,
                dry_run=dry_run,
                force=force,
                stats=stats,
            )

            if (i + 1) % batch_size == 0:
                self.stdout.write(f"  Progress: {i + 1}/{words.count()}")

            if not dry_run:
                time.sleep(delay)

        return stats

    def _cache_peppi_phrases(self, language: str, dry_run: bool, force: bool, delay: float, batch_size: int) -> dict:
        """Cache audio for Peppi phrases (currently Hindi only)."""
        stats = {'total': 0, 'cached': 0, 'generated': 0, 'failed': 0}

        # PeppiPhrase model currently only has Hindi text
        # Only cache for HINDI language
        if language != 'HINDI':
            self.stdout.write(f"  Peppi phrases only available in Hindi (skipping {language})")
            return stats

        phrases = PeppiPhrase.objects.filter(is_active=True)
        self.stdout.write(f"  Found {phrases.count()} Peppi phrases")

        for i, phrase in enumerate(phrases):
            if phrase.text_hindi:
                stats['total'] += 1
                self._generate_audio(
                    text=phrase.text_hindi,
                    language='HINDI',
                    content_type='peppi_phrase',
                    content_id=f"peppi_{phrase.category}_{phrase.id}",
                    dry_run=dry_run,
                    force=force,
                    stats=stats,
                )

            if (i + 1) % batch_size == 0:
                self.stdout.write(f"  Progress: {i + 1}/{phrases.count()}")

            if not dry_run:
                time.sleep(delay)

        return stats

    def _generate_audio(
        self,
        text: str,
        language: str,
        content_type: str,
        content_id: str,
        dry_run: bool,
        force: bool,
        stats: dict,
    ):
        """Generate and cache audio for a single text item."""
        voice_style = 'kid_friendly'
        cache_key = TTSService._generate_cache_key(text, language, voice_style)

        # Check if already cached
        if not force:
            existing = AudioCache.objects.filter(cache_key=cache_key).first()
            if existing and existing.audio_file:
                stats['cached'] += 1
                return

        if dry_run:
            self.stdout.write(f"    [DRY-RUN] {text[:30]}...")
            return

        try:
            # Use Svara TTS (mock user with svara provider)
            from unittest.mock import Mock
            mock_user = Mock()
            mock_user.tts_provider = 'svara'

            audio_bytes, provider, was_cached = TTSService.get_audio(
                text=text,
                language=language,
                voice_profile=voice_style,
                user=mock_user,
                force_regenerate=force,
            )

            # Update cache entry with content metadata
            AudioCache.objects.filter(cache_key=cache_key).update(
                content_type=content_type,
                content_id=content_id,
            )

            stats['generated'] += 1

        except TTSServiceError as e:
            self.stdout.write(self.style.ERROR(f"    [FAIL] {text[:20]}... - {e}"))
            stats['failed'] += 1
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"    [ERROR] {text[:20]}... - {e}"))
            stats['failed'] += 1
