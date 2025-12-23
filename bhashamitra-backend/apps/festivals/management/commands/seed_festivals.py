"""Management command to seed festival data."""
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.festivals.models import Festival, FestivalActivity
from apps.festivals.data.festivals import FESTIVALS_DATA, DIWALI_ACTIVITIES


class Command(BaseCommand):
    """Seed festivals and activities into the database."""

    help = 'Seed festival data including activities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing festival data before seeding',
        )
        parser.add_argument(
            '--activities-only',
            action='store_true',
            help='Only seed activities (assumes festivals exist)',
        )

    def handle(self, *args, **options):
        """Execute the command."""
        if options['clear']:
            self.stdout.write('Clearing existing festival data...')
            FestivalActivity.objects.all().delete()
            Festival.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared all festival data.'))

        if options['activities_only']:
            self._seed_activities()
        else:
            self._seed_festivals()
            self._seed_activities()

        self.stdout.write(self.style.SUCCESS('Festival seeding complete!'))

    @transaction.atomic
    def _seed_festivals(self):
        """Seed festival records."""
        created_count = 0
        updated_count = 0

        for festival_data in FESTIVALS_DATA:
            festival, created = Festival.objects.update_or_create(
                name=festival_data['name'],
                defaults={
                    'name_native': festival_data.get('name_native', ''),
                    'name_hindi': festival_data.get('name_hindi', ''),
                    'name_tamil': festival_data.get('name_tamil', ''),
                    'name_gujarati': festival_data.get('name_gujarati', ''),
                    'name_punjabi': festival_data.get('name_punjabi', ''),
                    'name_telugu': festival_data.get('name_telugu', ''),
                    'name_malayalam': festival_data.get('name_malayalam', ''),
                    'religion': festival_data['religion'],
                    'description': festival_data.get('description', ''),
                    'significance': festival_data.get('significance', ''),
                    'typical_month': festival_data.get('typical_month', 1),
                    'is_lunar_calendar': festival_data.get('is_lunar_calendar', False),
                    'image_url': festival_data.get('image_url'),
                    'is_active': True,
                }
            )

            if created:
                created_count += 1
                self.stdout.write(f'  Created: {festival.name}')
            else:
                updated_count += 1
                self.stdout.write(f'  Updated: {festival.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Festivals: {created_count} created, {updated_count} updated'
            )
        )

    @transaction.atomic
    def _seed_activities(self):
        """Seed festival activities."""
        # Get Diwali festival
        try:
            diwali = Festival.objects.get(name='Diwali')
        except Festival.DoesNotExist:
            self.stdout.write(
                self.style.WARNING('Diwali festival not found. Skipping activities.')
            )
            return

        created_count = 0
        for activity_data in DIWALI_ACTIVITIES:
            activity, created = FestivalActivity.objects.update_or_create(
                festival=diwali,
                title=activity_data['title'],
                defaults={
                    'activity_type': activity_data['activity_type'],
                    'description': activity_data['description'],
                    'instructions': activity_data['instructions'],
                    'materials_needed': activity_data.get('materials_needed', []),
                    'min_age': activity_data.get('min_age', 3),
                    'max_age': activity_data.get('max_age', 8),
                    'duration_minutes': activity_data.get('duration_minutes', 15),
                    'difficulty_level': activity_data.get('difficulty_level', 1),
                    'points_reward': activity_data.get('points_reward', 25),
                    'is_active': True,
                }
            )
            if created:
                created_count += 1
                self.stdout.write(f'  Created activity: {activity.title}')

        self.stdout.write(
            self.style.SUCCESS(f'Activities: {created_count} created for Diwali')
        )

        # Add sample activities for other major festivals
        self._seed_other_festival_activities()

    def _seed_other_festival_activities(self):
        """Seed sample activities for other major festivals."""
        other_activities = {
            'Holi': [
                {
                    'title': 'Colors of Holi',
                    'activity_type': 'VOCABULARY',
                    'description': 'Learn color names in different languages',
                    'instructions': 'Match colors with their names',
                    'min_age': 3,
                    'max_age': 8,
                    'points_reward': 20,
                },
                {
                    'title': 'Holi Story Time',
                    'activity_type': 'STORY',
                    'description': 'The story of Holika and Prahlad',
                    'instructions': 'Listen to the magical story of why we celebrate Holi',
                    'min_age': 4,
                    'max_age': 8,
                    'points_reward': 30,
                },
            ],
            'Eid ul-Fitr': [
                {
                    'title': 'Eid Greetings',
                    'activity_type': 'VOCABULARY',
                    'description': 'Learn Eid greetings in different languages',
                    'instructions': 'Practice saying Eid Mubarak in various ways',
                    'min_age': 3,
                    'max_age': 8,
                    'points_reward': 20,
                },
            ],
            'Christmas': [
                {
                    'title': 'Christmas Carols',
                    'activity_type': 'SONG',
                    'description': 'Sing along to popular Christmas songs',
                    'instructions': 'Listen and sing along with the lyrics',
                    'min_age': 3,
                    'max_age': 8,
                    'points_reward': 25,
                },
            ],
            'Baisakhi': [
                {
                    'title': 'Bhangra Dance',
                    'activity_type': 'GAME',
                    'description': 'Learn simple Bhangra moves',
                    'instructions': 'Follow the dance steps shown on screen',
                    'min_age': 4,
                    'max_age': 8,
                    'points_reward': 30,
                },
            ],
        }

        created_count = 0
        for festival_name, activities in other_activities.items():
            try:
                festival = Festival.objects.get(name=festival_name)
                for activity_data in activities:
                    activity, created = FestivalActivity.objects.update_or_create(
                        festival=festival,
                        title=activity_data['title'],
                        defaults={
                            'activity_type': activity_data['activity_type'],
                            'description': activity_data['description'],
                            'instructions': activity_data['instructions'],
                            'materials_needed': activity_data.get('materials_needed', []),
                            'min_age': activity_data.get('min_age', 3),
                            'max_age': activity_data.get('max_age', 8),
                            'duration_minutes': activity_data.get('duration_minutes', 15),
                            'difficulty_level': activity_data.get('difficulty_level', 1),
                            'points_reward': activity_data.get('points_reward', 25),
                            'is_active': True,
                        }
                    )
                    if created:
                        created_count += 1
            except Festival.DoesNotExist:
                continue

        self.stdout.write(
            self.style.SUCCESS(f'Other festival activities: {created_count} created')
        )
