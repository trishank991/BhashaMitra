"""
Comprehensive production seeding command for BhashaMitra.

This single command runs all necessary seed scripts in the correct order
to set up a fully functional BhashaMitra production database.

Usage:
    python manage.py seed_production              # Seed everything
    python manage.py seed_production --curriculum # Only curriculum data
    python manage.py seed_production --festivals  # Only festival data
    python manage.py seed_production --content    # Only content (vocab, grammar, stories)
    python manage.py seed_production --dry-run    # Show what would be seeded
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import transaction
import sys


class Command(BaseCommand):
    help = 'Seed production database with all required data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--curriculum',
            action='store_true',
            help='Seed only curriculum data (levels, modules, lessons)'
        )
        parser.add_argument(
            '--festivals',
            action='store_true',
            help='Seed only festival data and stories'
        )
        parser.add_argument(
            '--content',
            action='store_true',
            help='Seed only content (vocabulary, grammar, games, assessments)'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be seeded without making changes'
        )
        parser.add_argument(
            '--language',
            type=str,
            default='HINDI',
            choices=['HINDI', 'TAMIL', 'GUJARATI', 'PUNJABI', 'ALL'],
            help='Language to seed (default: HINDI)'
        )

    def handle(self, *args, **options):
        dry_run = options.get('dry_run', False)
        seed_curriculum = options.get('curriculum', False)
        seed_festivals = options.get('festivals', False)
        seed_content = options.get('content', False)
        language = options.get('language', 'HINDI')

        # If no specific option, seed everything
        seed_all = not (seed_curriculum or seed_festivals or seed_content)

        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS(
            '  BHASHAMITRA PRODUCTION DATABASE SEEDING'
        ))
        self.stdout.write('=' * 70 + '\n')

        if dry_run:
            self.stdout.write(self.style.WARNING('DRY RUN MODE - No changes will be made\n'))
            self.show_dry_run(seed_all, seed_curriculum, seed_festivals, seed_content, language)
            return

        try:
            with transaction.atomic():
                # 1. CURRICULUM STRUCTURE
                if seed_all or seed_curriculum:
                    self.seed_curriculum(language)

                # 2. CONTENT (Vocabulary, Grammar, Games)
                if seed_all or seed_content:
                    self.seed_content()

                # 3. FESTIVALS AND STORIES
                if seed_all or seed_festivals:
                    self.seed_festivals()

                # 4. BASE DATA (Badges, etc.)
                if seed_all:
                    self.seed_base_data()

            self.print_summary()

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'\nSeeding failed: {str(e)}'))
            self.stdout.write('Rolling back all changes...')
            raise

    def seed_curriculum(self, language: str):
        """Seed curriculum structure (levels, modules, lessons)."""
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.HTTP_INFO('STEP 1: CURRICULUM STRUCTURE'))
        self.stdout.write('-' * 50)

        # 1a. Seed L1-L10 Level definitions
        self.stdout.write('  [1/4] Seeding curriculum levels (L1-L10)...')
        try:
            call_command('seed_curriculum_levels', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 1b. Seed L1-L2 modules and lessons (Hindi)
        self.stdout.write('  [2/4] Seeding L1-L2 curriculum (modules, lessons, vocab)...')
        try:
            call_command('seed_l1_l2_curriculum', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 1c. Seed language-specific curriculum
        if language == 'ALL':
            languages = ['TAMIL', 'GUJARATI', 'PUNJABI']
        else:
            languages = [language] if language != 'HINDI' else []

        for lang in languages:
            lang_lower = lang.lower()
            cmd_name = f'seed_{lang_lower}_l1_l2'
            self.stdout.write(f'  [3/4] Seeding {lang} L1-L2 curriculum...')
            try:
                call_command(cmd_name, verbosity=0)
                self.stdout.write(self.style.SUCCESS('       Done'))
            except Exception as e:
                self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 1d. Seed L1 songs and stories
        self.stdout.write('  [4/4] Seeding L1 songs and stories...')
        try:
            call_command('seed_l1_songs_stories', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

    def seed_content(self):
        """Seed content data (vocabulary, grammar, games, assessments)."""
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.HTTP_INFO('STEP 2: CONTENT DATA'))
        self.stdout.write('-' * 50)

        # 2a. Grammar content
        self.stdout.write('  [1/4] Seeding grammar content...')
        try:
            call_command('seed_grammar_content', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 2b. Games
        self.stdout.write('  [2/4] Seeding games...')
        try:
            call_command('seed_games', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 2c. Assessments
        self.stdout.write('  [3/4] Seeding assessments...')
        try:
            call_command('seed_assessments', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 2d. Verified Hindi alphabet
        self.stdout.write('  [4/4] Seeding verified Hindi alphabet...')
        try:
            call_command('seed_verified_hindi', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

    def seed_festivals(self):
        """Seed festivals and festival stories."""
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.HTTP_INFO('STEP 3: FESTIVALS & STORIES'))
        self.stdout.write('-' * 50)

        # 3a. Base festivals data (26 Indian festivals)
        self.stdout.write('  [1/3] Seeding festivals (26 festivals)...')
        try:
            call_command('seed_festivals', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 3b. Diwali story
        self.stdout.write('  [2/3] Seeding Diwali story...')
        try:
            call_command('seed_diwali', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 3c. Festival stories (Holi, Raksha Bandhan, etc.)
        self.stdout.write('  [3/3] Seeding festival stories (7 festivals)...')
        try:
            call_command('seed_festival_stories', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

    def seed_base_data(self):
        """Seed base data like badges, etc."""
        self.stdout.write('\n' + '-' * 50)
        self.stdout.write(self.style.HTTP_INFO('STEP 4: BASE DATA'))
        self.stdout.write('-' * 50)

        # 4a. Badges (using script)
        self.stdout.write('  [1/2] Seeding badges...')
        try:
            from scripts.seed_badges import seed_badges
            count = seed_badges()
            self.stdout.write(self.style.SUCCESS(f'       Done ({count} badges)'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

        # 4b. Parent activities
        self.stdout.write('  [2/2] Seeding parent activities...')
        try:
            call_command('seed_parent_activities', verbosity=0)
            self.stdout.write(self.style.SUCCESS('       Done'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'       Skipped: {e}'))

    def show_dry_run(self, seed_all, seed_curriculum, seed_festivals, seed_content, language):
        """Show what would be seeded in dry run mode."""
        self.stdout.write('The following would be seeded:\n')

        if seed_all or seed_curriculum:
            self.stdout.write('  CURRICULUM:')
            self.stdout.write('    - 10 Curriculum Levels (L1-L10)')
            self.stdout.write('    - L1-L2 Modules and Lessons')
            if language == 'ALL':
                self.stdout.write('    - Tamil, Gujarati, Punjabi L1-L2')
            elif language != 'HINDI':
                self.stdout.write(f'    - {language} L1-L2')
            self.stdout.write('    - L1 Songs and Stories')
            self.stdout.write('')

        if seed_all or seed_content:
            self.stdout.write('  CONTENT:')
            self.stdout.write('    - Grammar topics and exercises')
            self.stdout.write('    - Interactive games')
            self.stdout.write('    - Assessment questions')
            self.stdout.write('    - Hindi alphabet with verified audio')
            self.stdout.write('')

        if seed_all or seed_festivals:
            self.stdout.write('  FESTIVALS:')
            self.stdout.write('    - 26 Indian festivals')
            self.stdout.write('    - Festival activities')
            self.stdout.write('    - 8 festival stories (Diwali, Holi, Raksha Bandhan,')
            self.stdout.write('      Janmashtami, Ganesh Chaturthi, Navratri, Christmas, Eid)')
            self.stdout.write('')

        if seed_all:
            self.stdout.write('  BASE DATA:')
            self.stdout.write('    - Achievement badges')
            self.stdout.write('    - Parent engagement activities')
            self.stdout.write('')

    def print_summary(self):
        """Print seeding summary."""
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS(
            '  SEEDING COMPLETE!'
        ))
        self.stdout.write('=' * 70)

        self.stdout.write('\nNext steps:')
        self.stdout.write('  1. Verify data in Django admin: /admin/')
        self.stdout.write('  2. Test curriculum navigation in frontend')
        self.stdout.write('  3. Test festival stories with Peppi narration')
        self.stdout.write('  4. Create test user accounts if needed')
        self.stdout.write('\nIf you encounter issues, run: python manage.py check\n')
