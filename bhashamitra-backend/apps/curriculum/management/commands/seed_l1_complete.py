"""
Master command to seed all L1 curriculum content.
Run: python manage.py seed_l1_complete

This runs all L1 seed commands in the correct order:
1. seed_curriculum_levels (prerequisite)
2. seed_l1_content (vocabulary, letters, matras)
3. seed_l1_modules_and_lessons (modules, lessons, content links)
4. seed_games (12 educational games)
5. seed_assessments (6 assessments, 100+ questions)
"""

from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connection


class Command(BaseCommand):
    help = 'Seed all L1 curriculum content (master command)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--skip-levels',
            action='store_true',
            help='Skip seeding curriculum levels (if already seeded)',
        )
        parser.add_argument(
            '--skip-content',
            action='store_true',
            help='Skip seeding L1 content (vocabulary, letters)',
        )
        parser.add_argument(
            '--only-games',
            action='store_true',
            help='Only seed games',
        )
        parser.add_argument(
            '--only-assessments',
            action='store_true',
            help='Only seed assessments',
        )

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('L1 CURRICULUM COMPLETE SEED'))
        self.stdout.write('=' * 60)
        self.stdout.write('')

        commands_to_run = []

        if options.get('only_games'):
            commands_to_run = [('seed_games', 'Educational Games')]
        elif options.get('only_assessments'):
            commands_to_run = [('seed_assessments', 'Assessments & Questions')]
        else:
            # Full seed sequence
            if not options.get('skip_levels'):
                commands_to_run.append(('seed_curriculum_levels', 'Curriculum Levels (L1-L10)'))

            if not options.get('skip_content'):
                commands_to_run.append(('seed_l1_content', 'L1 Content (Vocabulary, Letters, Matras)'))

            commands_to_run.extend([
                ('seed_l1_modules_and_lessons', 'L1 Modules, Lessons & Content Links'),
                ('seed_l1_songs_stories', 'L1 Songs, Stories & Peppi Phrases'),
                ('seed_games', 'Educational Games'),
                ('seed_assessments', 'Assessments & Questions'),
            ])

        total_commands = len(commands_to_run)
        successful = 0
        failed = []

        for idx, (cmd, description) in enumerate(commands_to_run, 1):
            self.stdout.write('')
            self.stdout.write(f'[{idx}/{total_commands}] {description}')
            self.stdout.write('-' * 40)

            try:
                call_command(cmd, stdout=self.stdout, stderr=self.stderr)
                successful += 1
                self.stdout.write(self.style.SUCCESS(f'  Completed: {cmd}'))
            except Exception as e:
                failed.append((cmd, str(e)))
                self.stdout.write(self.style.ERROR(f'  Failed: {cmd}'))
                self.stdout.write(self.style.ERROR(f'  Error: {str(e)}'))

        # Summary
        self.stdout.write('')
        self.stdout.write('=' * 60)
        self.stdout.write(self.style.SUCCESS('SEEDING COMPLETE - SUMMARY'))
        self.stdout.write('=' * 60)
        self.stdout.write(f'  Commands Run: {total_commands}')
        self.stdout.write(f'  Successful: {successful}')
        self.stdout.write(f'  Failed: {len(failed)}')

        if failed:
            self.stdout.write('')
            self.stdout.write(self.style.ERROR('Failed Commands:'))
            for cmd, error in failed:
                self.stdout.write(f'  - {cmd}: {error}')

        # Database Stats
        self.stdout.write('')
        self.stdout.write('Database Statistics:')
        self._print_db_stats()

    def _print_db_stats(self):
        """Print current database statistics."""
        try:
            from apps.curriculum.models import (
                CurriculumLevel, CurriculumModule, Lesson, LessonContent,
                Game, Assessment, AssessmentQuestion,
                VocabularyWord, Letter, Matra, Song, PeppiPhrase
            )
            from apps.stories.models import Story, StoryPage

            stats = [
                ('Curriculum Levels', CurriculumLevel.objects.count()),
                ('Modules', CurriculumModule.objects.count()),
                ('Lessons', Lesson.objects.count()),
                ('Lesson Content Links', LessonContent.objects.count()),
                ('Songs', Song.objects.count()),
                ('Stories', Story.objects.count()),
                ('Story Pages', StoryPage.objects.count()),
                ('Games', Game.objects.count()),
                ('Assessments', Assessment.objects.count()),
                ('Assessment Questions', AssessmentQuestion.objects.count()),
                ('Vocabulary Words', VocabularyWord.objects.count()),
                ('Letters', Letter.objects.count()),
                ('Matras', Matra.objects.count()),
                ('Peppi Phrases', PeppiPhrase.objects.count()),
            ]

            for name, count in stats:
                self.stdout.write(f'  {name}: {count}')

        except Exception as e:
            self.stdout.write(f'  Error getting stats: {str(e)}')
