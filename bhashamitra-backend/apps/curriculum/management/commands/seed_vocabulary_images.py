"""Seed vocabulary words with image URLs from free image sources."""
from django.core.management.base import BaseCommand
from apps.curriculum.models import VocabularyWord
import urllib.parse


class Command(BaseCommand):
    help = 'Add image URLs to vocabulary words using free image APIs'

    # Category-specific image keywords for better image matching
    CATEGORY_KEYWORDS = {
        'Family': 'family,people,portrait',
        'Colors': 'colorful,paint,abstract',
        'Numbers': 'numbers,counting,math',
        'Animals': 'animal,wildlife,pet',
        'Food': 'food,fruit,vegetable,meal',
        'Body Parts': 'human,body,anatomy',
        'Greetings': 'hello,wave,greeting,smile',
        'Actions': 'action,motion,activity',
    }

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            default='HINDI',
            help='Language to update (default: HINDI)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes'
        )
        parser.add_argument(
            '--theme',
            type=str,
            help='Only update words from specific theme'
        )
        parser.add_argument(
            '--source',
            type=str,
            default='unsplash',
            choices=['unsplash', 'picsum', 'picsum-seed'],
            help='Image source API to use (default: unsplash)'
        )
        parser.add_argument(
            '--overwrite',
            action='store_true',
            help='Overwrite existing image URLs'
        )
        parser.add_argument(
            '--validate',
            action='store_true',
            help='Validate that URLs return valid images (requires requests library)'
        )

    def handle(self, *args, **options):
        language = options['language']
        dry_run = options['dry_run']
        theme_filter = options.get('theme')
        source = options['source']
        overwrite = options['overwrite']
        validate = options['validate']

        # Query words without images
        if overwrite:
            queryset = VocabularyWord.objects.filter(
                theme__language=language
            )
        else:
            queryset = VocabularyWord.objects.filter(
                theme__language=language,
                image_url__isnull=True
            ) | VocabularyWord.objects.filter(
                theme__language=language,
                image_url=''
            )

        if theme_filter:
            queryset = queryset.filter(theme__name__icontains=theme_filter)

        words = queryset.select_related('theme')
        total = words.count()

        self.stdout.write(self.style.NOTICE(f'Found {total} words to update'))

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN - no changes will be made'))

        self.stdout.write('')

        updated = 0
        skipped = 0
        failed = 0

        for word in words:
            try:
                # Generate image URL based on source
                image_url = self._generate_image_url(word, source)

                # Validate URL if requested
                if validate and not self._validate_url(image_url):
                    self.stdout.write(
                        self.style.ERROR(f'  [{updated + skipped + failed + 1}/{total}] FAILED: {word.word} - Invalid URL')
                    )
                    failed += 1
                    continue

                # Display keyword for context
                keyword = self._get_search_keyword(word)

                if not dry_run:
                    word.image_url = image_url
                    word.save(update_fields=['image_url'])

                updated += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  [{updated + skipped + failed}/{total}] {word.word} ({word.theme.name}) -> {keyword}')
                )

            except Exception as e:
                failed += 1
                self.stdout.write(
                    self.style.ERROR(f'  [{updated + skipped + failed}/{total}] ERROR: {word.word} - {str(e)}')
                )

        # Print summary
        self.stdout.write('')
        self.stdout.write('=' * 60)
        if dry_run:
            self.stdout.write(self.style.WARNING(f'DRY RUN COMPLETE - No changes made'))
        else:
            self.stdout.write(self.style.SUCCESS(f'SEEDING COMPLETE'))

        self.stdout.write(f'  Total words processed: {total}')
        self.stdout.write(self.style.SUCCESS(f'  Successfully updated: {updated}'))
        if skipped > 0:
            self.stdout.write(self.style.WARNING(f'  Skipped: {skipped}'))
        if failed > 0:
            self.stdout.write(self.style.ERROR(f'  Failed: {failed}'))
        self.stdout.write('=' * 60)

    def _get_search_keyword(self, word):
        """Generate search keyword from word translation and theme."""
        # Start with translation
        keyword = word.translation.lower().strip()

        # Remove special characters and parentheses content (e.g., "one (1)" -> "one")
        keyword = keyword.split('(')[0].strip()

        # Remove special characters but keep spaces
        keyword = ''.join(c for c in keyword if c.isalnum() or c == ' ')

        # Add theme-specific keywords if available
        theme_name = word.theme.name
        if theme_name in self.CATEGORY_KEYWORDS:
            keyword = f"{keyword},{self.CATEGORY_KEYWORDS[theme_name]}"

        return keyword

    def _generate_image_url(self, word, source):
        """Generate image URL based on the selected source."""
        keyword = self._get_search_keyword(word)

        if source == 'unsplash':
            # Use Lorem Picsum as primary (more reliable than Unsplash Source which is deprecated)
            # Seed based on keyword hash for consistent images
            import hashlib
            seed = int(hashlib.md5(keyword.encode()).hexdigest()[:8], 16) % 1000
            return f'https://picsum.photos/seed/{seed}/400/300'

        elif source == 'picsum':
            # Lorem Picsum with random image
            return 'https://picsum.photos/400/300'

        elif source == 'picsum-seed':
            # Lorem Picsum with seed based on word ID for consistency
            return f'https://picsum.photos/seed/{word.id}/400/300'

        else:
            raise ValueError(f'Unknown source: {source}')

    def _validate_url(self, url):
        """Validate that URL returns a valid image (optional feature)."""
        try:
            import requests
            response = requests.head(url, timeout=5, allow_redirects=True)
            content_type = response.headers.get('content-type', '')
            return response.status_code == 200 and 'image' in content_type
        except ImportError:
            self.stdout.write(
                self.style.WARNING('  WARNING: requests library not installed, skipping validation')
            )
            return True
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'  WARNING: Validation failed for {url}: {str(e)}')
            )
            return False
