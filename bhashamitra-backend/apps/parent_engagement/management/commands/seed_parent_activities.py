"""Management command to seed parent-child activity data."""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.parent_engagement.models import ParentChildActivity
from apps.parent_engagement.data.parent_activities import PARENT_ACTIVITIES


class Command(BaseCommand):
    """Seed parent-child activities into the database."""

    help = 'Seed parent-child activity suggestions'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing activities before seeding',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        if options['clear']:
            self.stdout.write('Clearing existing parent activities...')
            ParentChildActivity.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all parent activities.'))

        self._seed_activities()
        self.stdout.write(self.style.SUCCESS('Parent activities seeding complete!'))

    @transaction.atomic
    def _seed_activities(self):
        """Seed parent-child activities."""
        created_count = 0

        for activity_data in PARENT_ACTIVITIES:
            activity, created = ParentChildActivity.objects.update_or_create(
                title=activity_data['title'],
                activity_type=activity_data['activity_type'],
                language=activity_data.get('language', 'ALL'),
                defaults={
                    'description': activity_data['description'],
                    'min_age': activity_data.get('min_age', 2),
                    'max_age': activity_data.get('max_age', 18),
                    'duration_minutes': activity_data.get('duration_minutes', 15),
                    'materials_needed': activity_data.get('materials_needed', []),
                    'learning_outcomes': activity_data.get('learning_outcomes', []),
                    'is_featured': activity_data.get('is_featured', False),
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  Created: {activity.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Total activities created: {created_count}')
        )
