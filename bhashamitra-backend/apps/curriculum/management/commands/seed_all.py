"""Management command to seed all BhashaMitra data."""
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Seed all BhashaMitra data (badges, alphabet, vocabulary, stories)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--badges',
            action='store_true',
            help='Seed badges only'
        )
        parser.add_argument(
            '--alphabet',
            action='store_true',
            help='Seed Hindi alphabet only'
        )
        parser.add_argument(
            '--vocabulary',
            action='store_true',
            help='Seed vocabulary only'
        )
        parser.add_argument(
            '--stories',
            action='store_true',
            help='Sync stories from StoryWeaver (requires internet)'
        )
        parser.add_argument(
            '--stories-limit',
            type=int,
            default=25,
            help='Number of stories to sync per language/level (default: 25)'
        )

    def handle(self, *args, **options):
        from scripts.seed_badges import seed_badges
        from scripts.seed_hindi_alphabet import seed_hindi_alphabet
        from scripts.seed_vocabulary import seed_vocabulary

        # If no specific option selected, seed local data only (not stories)
        seed_everything = not any([
            options['badges'],
            options['alphabet'],
            options['vocabulary'],
            options['stories']
        ])

        self.stdout.write(self.style.NOTICE('Starting BhashaMitra data seeding...'))
        self.stdout.write('')

        if options['badges'] or seed_everything:
            self.stdout.write('Seeding badges...')
            count = seed_badges()
            self.stdout.write(self.style.SUCCESS(f'  -> {count} badges seeded'))

        if options['alphabet'] or seed_everything:
            self.stdout.write('Seeding Hindi alphabet...')
            count = seed_hindi_alphabet()
            self.stdout.write(self.style.SUCCESS(f'  -> {count} characters seeded'))

        if options['vocabulary'] or seed_everything:
            self.stdout.write('Seeding vocabulary...')
            count = seed_vocabulary()
            self.stdout.write(self.style.SUCCESS(f'  -> {count} words seeded'))

        if options['stories']:
            self.stdout.write('')
            self.stdout.write('Syncing stories from StoryWeaver...')
            self.stdout.write('(This requires internet connection)')
            call_command(
                'sync_stories',
                language='HINDI',
                limit=options['stories_limit'],
                skip_existing=True,
                verbosity=1
            )

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('All seeding complete!'))
