"""
Management command to pre-generate TTS audio for all stories.
Run this after syncing new stories from StoryWeaver.

Usage:
    python manage.py prewarm_tts_cache
    python manage.py prewarm_tts_cache --language=HINDI
    python manage.py prewarm_tts_cache --story-id=xxx
"""
import time
from django.core.management.base import BaseCommand
from apps.stories.models import Story
from apps.speech.services.tts_service import TTSService


class Command(BaseCommand):
    help = 'Pre-generate and cache TTS audio for stories'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Only process stories in this language (HINDI, TAMIL, etc.)'
        )
        parser.add_argument(
            '--story-id',
            type=str,
            help='Process a specific story only'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=None,
            help='Maximum number of stories to process'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually generating audio'
        )

    def handle(self, *args, **options):
        language = options.get('language')
        story_id = options.get('story_id')
        limit = options.get('limit')
        dry_run = options.get('dry_run')

        # Build queryset
        stories = Story.objects.prefetch_related('pages')

        if story_id:
            stories = stories.filter(id=story_id)
        elif language:
            stories = stories.filter(language=language)

        if limit:
            stories = stories[:limit]

        total_stories = stories.count()
        total_pages = 0
        total_generated = 0
        total_cached = 0
        total_failed = 0
        total_cost = 0

        self.stdout.write(f"\nPre-warming TTS cache for {total_stories} stories\n")

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - No audio will be generated\n"))

        for i, story in enumerate(stories, 1):
            self.stdout.write(f"\n[{i}/{total_stories}] {story.title}")
            self.stdout.write(f"    Language: {story.language}, Pages: {story.pages.count()}")

            if dry_run:
                total_pages += story.pages.count()
                continue

            try:
                results = TTSService.prewarm_story(str(story.id))

                total_pages += results['pages_total']
                total_generated += results['pages_generated']
                total_cached += results['pages_cached']
                total_failed += results['pages_failed']
                total_cost += results['total_cost_usd']

                self.stdout.write(
                    f"    Generated: {results['pages_generated']}, "
                    f"Cached: {results['pages_cached']}, "
                    f"Failed: {results['pages_failed']}"
                )

                # Rate limiting - be nice to the API
                if results['pages_generated'] > 0:
                    time.sleep(1)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    Error: {e}"))
                total_failed += story.pages.count()

        # Summary
        self.stdout.write(f"\n{'='*50}")
        self.stdout.write(f"Summary:")
        self.stdout.write(f"    Total Stories: {total_stories}")
        self.stdout.write(f"    Total Pages: {total_pages}")

        if not dry_run:
            self.stdout.write(f"    Pages Generated: {total_generated}")
            self.stdout.write(f"    Pages Already Cached: {total_cached}")
            self.stdout.write(f"    Pages Failed: {total_failed}")
            self.stdout.write(f"    Estimated Cost: ${total_cost:.4f}")

        self.stdout.write(self.style.SUCCESS(f"\nPre-warming complete!\n"))
