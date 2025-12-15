"""Management command to sync stories from StoryWeaver API."""
import time
from django.core.management.base import BaseCommand
from django.db import transaction
from external.storyweaver.client import StoryWeaverClient
from apps.stories.models import Story, StoryPage


class Command(BaseCommand):
    help = 'Sync stories from StoryWeaver API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            default='HINDI',
            choices=['HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'TELUGU', 'MALAYALAM'],
            help='Language to sync (default: HINDI)'
        )
        parser.add_argument(
            '--level',
            type=int,
            choices=[1, 2, 3, 4],
            help='Reading level to sync (1-4). If not specified, syncs all levels.'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of stories to sync (default: 50)'
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Skip stories that already exist in the database'
        )
        parser.add_argument(
            '--with-pages',
            action='store_true',
            default=True,
            help='Also fetch and sync story pages (default: True)'
        )

    def handle(self, *args, **options):
        language = options['language']
        level = options.get('level')
        limit = options['limit']
        skip_existing = options['skip_existing']
        with_pages = options['with_pages']

        client = StoryWeaverClient()
        synced_count = 0
        skipped_count = 0
        error_count = 0

        self.stdout.write('')
        self.stdout.write(self.style.NOTICE(
            f'Syncing {language} stories (level: {level or "all"}, limit: {limit})'
        ))
        self.stdout.write('')

        # If level specified, only sync that level; otherwise sync levels 1-4
        levels_to_sync = [level] if level else [1, 2, 3, 4]
        stories_per_level = limit // len(levels_to_sync)

        for current_level in levels_to_sync:
            self.stdout.write(f'Fetching Level {current_level} stories...')

            try:
                stories = client.get_stories(
                    language=language,
                    level=current_level,
                    limit=stories_per_level
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  Error fetching stories: {e}'))
                continue

            if not stories:
                self.stdout.write(f'  No stories found for Level {current_level}')
                continue

            self.stdout.write(f'  Found {len(stories)} stories')

            for story_data in stories:
                if synced_count >= limit:
                    break

                sw_id = story_data.get('storyweaver_id', '')
                title = story_data.get('title', 'Unknown')

                # Check if exists
                if skip_existing and Story.objects.filter(storyweaver_id=sw_id).exists():
                    skipped_count += 1
                    self.stdout.write(f'    [SKIP] {title}')
                    continue

                try:
                    story = self._sync_story(client, story_data, with_pages)
                    synced_count += 1
                    page_info = f" ({story.page_count} pages)" if with_pages else ""
                    self.stdout.write(self.style.SUCCESS(
                        f'    [OK] {title}{page_info}'
                    ))

                    # Rate limiting - be respectful to StoryWeaver API
                    time.sleep(0.3)

                except Exception as e:
                    error_count += 1
                    self.stdout.write(self.style.ERROR(
                        f'    [ERROR] {title}: {e}'
                    ))

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(
            f'Sync complete: {synced_count} synced, {skipped_count} skipped, {error_count} errors'
        ))
        self.stdout.write(f'Total stories in database: {Story.objects.count()}')
        self.stdout.write('')

    @transaction.atomic
    def _sync_story(self, client: StoryWeaverClient, story_data: dict, with_pages: bool) -> Story:
        """Sync a single story and optionally its pages."""
        sw_id = story_data['storyweaver_id']

        # Create or update story
        story, created = Story.objects.update_or_create(
            storyweaver_id=sw_id,
            defaults={
                'title': story_data.get('title', ''),
                'language': story_data.get('language', 'HINDI'),
                'level': story_data.get('level', 1),
                'page_count': story_data.get('page_count', 0),
                'cover_image_url': story_data.get('cover_image_url', ''),
                'synopsis': story_data.get('synopsis', ''),
                'author': story_data.get('author', ''),
                'categories': story_data.get('categories', []),
            }
        )

        # Fetch and sync pages if requested
        if with_pages:
            detail = client.get_story_detail(sw_id)
            if detail and 'pages' in detail:
                # Delete existing pages for update
                story.pages.all().delete()

                pages_data = detail.get('pages', [])
                for page_data in pages_data:
                    StoryPage.objects.create(
                        story=story,
                        page_number=page_data.get('page_number', 1),
                        text_content=page_data.get('text_content', ''),
                        image_url=page_data.get('image_url', ''),
                    )

                # Update page count from actual pages
                story.page_count = len(pages_data)
                story.save()

        return story
