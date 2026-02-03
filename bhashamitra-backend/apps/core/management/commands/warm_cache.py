"""Management command to warm curriculum cache."""
from django.core.management.base import BaseCommand
from apps.core.cache_service import warm_all_curriculum_caches, warm_curriculum_cache


class Command(BaseCommand):
    help = 'Pre-warm curriculum cache for all or specific languages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Specific language to warm (e.g., HINDI, TAMIL)',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Warm cache for all languages',
        )

    def handle(self, *args, **options):
        language = options.get('language')
        warm_all = options.get('all', False)

        if language:
            self.stdout.write(f'Warming cache for {language}...')
            try:
                stats = warm_curriculum_cache(language.upper())
                self.stdout.write(self.style.SUCCESS(
                    f"✓ {language}: {stats['scripts']} scripts, "
                    f"{stats['vocab_themes']} vocab themes, "
                    f"{stats['grammar_topics']} grammar topics, "
                    f"{stats['stories']} stories, "
                    f"{stats['games']} games"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ {language}: {e}'))

        elif warm_all:
            self.stdout.write('Warming cache for all languages...')
            results = warm_all_curriculum_caches()

            for stats in results:
                if 'error' in stats:
                    self.stdout.write(self.style.ERROR(
                        f"✗ {stats['language']}: {stats['error']}"
                    ))
                else:
                    self.stdout.write(self.style.SUCCESS(
                        f"✓ {stats['language']}: {stats['scripts']} scripts, "
                        f"{stats['vocab_themes']} vocab themes, "
                        f"{stats['grammar_topics']} grammar topics, "
                        f"{stats['stories']} stories, "
                        f"{stats['games']} games"
                    ))

            self.stdout.write(self.style.SUCCESS('\nCache warming complete!'))

        else:
            self.stdout.write(self.style.WARNING(
                'Please specify --language=HINDI or --all'
            ))
