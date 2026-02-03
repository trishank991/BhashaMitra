"""Seed curriculum levels L1-L10."""
from django.core.management.base import BaseCommand
from apps.curriculum.models.level import CurriculumLevel


class Command(BaseCommand):
    help = 'Seed curriculum levels L1-L10'

    def handle(self, *args, **options):
        levels_data = [
            {
                'code': 'L1',
                'name_english': 'Ankur (Sprout)',
                'name_hindi': 'अंकुर',
                'name_romanized': 'Ankur',
                'min_age': 4,
                'max_age': 5,
                'description': 'Introduction to Hindi sounds, basic words, and cultural context through play.',
                'learning_objectives': [
                    'Recognize basic Hindi sounds and letters',
                    'Learn 50+ everyday words',
                    'Understand simple greetings',
                    'Develop listening skills through songs',
                ],
                'peppi_welcome': "Namaste! I'm Peppi! Let's start our Hindi adventure together!",
                'peppi_completion': "Amazing work! You've sprouted into a Hindi learner!",
                'emoji': '🌱',
                'theme_color': '#86efac',
                'order': 1,
                'estimated_hours': 15,
            },
            {
                'code': 'L2',
                'name_english': 'Paudha (Seedling)',
                'name_hindi': 'पौधा',
                'name_romanized': 'Paudha',
                'min_age': 5,
                'max_age': 6,
                'description': 'Building vocabulary, simple sentences, and cultural awareness.',
                'learning_objectives': [
                    'Master Devanagari alphabet basics',
                    'Learn 100+ vocabulary words',
                    'Form simple sentences',
                    'Understand basic grammar patterns',
                ],
                'peppi_welcome': 'Welcome back! Ready to grow your Hindi skills?',
                'peppi_completion': "You're growing strong in Hindi!",
                'emoji': '🌿',
                'theme_color': '#4ade80',
                'order': 2,
                'estimated_hours': 20,
            },
            {
                'code': 'L3',
                'name_english': 'Vriksh (Tree)',
                'name_hindi': 'वृक्ष',
                'name_romanized': 'Vriksh',
                'min_age': 6,
                'max_age': 7,
                'description': 'Reading simple stories, expressing ideas, and cultural traditions.',
                'learning_objectives': [
                    'Read simple Hindi stories',
                    'Write basic sentences',
                    'Learn 150+ new words',
                    'Understand cultural festivals',
                ],
                'peppi_welcome': "You're becoming strong like a tree!",
                'peppi_completion': 'Your Hindi roots are strong now!',
                'emoji': '🌳',
                'theme_color': '#22c55e',
                'order': 3,
                'estimated_hours': 25,
            },
            {
                'code': 'L4',
                'name_english': 'Pushp (Flower)',
                'name_hindi': 'पुष्प',
                'name_romanized': 'Pushp',
                'min_age': 7,
                'max_age': 8,
                'description': 'Creative expression, storytelling, and cultural exploration.',
                'learning_objectives': [
                    'Create your own Hindi stories',
                    'Use descriptive language',
                    'Learn 200+ advanced words',
                    'Explore Indian culture deeply',
                ],
                'peppi_welcome': 'Time to bloom with beautiful Hindi!',
                'peppi_completion': "You're blooming beautifully in Hindi!",
                'emoji': '🌻',
                'theme_color': '#fbbf24',
                'order': 4,
                'estimated_hours': 30,
            },
            {
                'code': 'L5',
                'name_english': 'Tara (Star)',
                'name_hindi': 'तारा',
                'name_romanized': 'Tara',
                'min_age': 8,
                'max_age': 9,
                'description': 'Advanced grammar, complex sentences, and creative writing.',
                'learning_objectives': [
                    'Master complex grammar structures',
                    'Write creative compositions',
                    'Learn 250+ vocabulary words',
                    'Understand Hindi literature basics',
                ],
                'peppi_welcome': "You're shining bright like a star!",
                'peppi_completion': "You're a Hindi star now!",
                'emoji': '⭐',
                'theme_color': '#facc15',
                'order': 5,
                'estimated_hours': 35,
            },
            {
                'code': 'L6',
                'name_english': 'Jyoti (Light)',
                'name_hindi': 'ज्योति',
                'name_romanized': 'Jyoti',
                'min_age': 9,
                'max_age': 10,
                'description': 'Literary analysis, advanced conversation, and cultural depth.',
                'learning_objectives': [
                    'Analyze Hindi literature',
                    'Engage in advanced conversations',
                    'Learn 300+ sophisticated words',
                    'Understand cultural nuances',
                ],
                'peppi_welcome': 'Your Hindi knowledge lights the way!',
                'peppi_completion': "You're illuminating Hindi brilliantly!",
                'emoji': '🔥',
                'theme_color': '#fb923c',
                'order': 6,
                'estimated_hours': 40,
            },
            {
                'code': 'L7',
                'name_english': 'Shikhar (Peak)',
                'name_hindi': 'शिखर',
                'name_romanized': 'Shikhar',
                'min_age': 10,
                'max_age': 11,
                'description': 'Advanced proficiency, literary excellence, and cultural mastery.',
                'learning_objectives': [
                    'Master advanced literary forms',
                    'Debate and discuss in Hindi',
                    'Learn 350+ advanced vocabulary',
                    'Understand poetry and prose',
                ],
                'peppi_welcome': 'Climbing to new heights in Hindi!',
                'peppi_completion': "You've reached amazing heights!",
                'emoji': '🏔️',
                'theme_color': '#60a5fa',
                'order': 7,
                'estimated_hours': 45,
            },
            {
                'code': 'L8',
                'name_english': 'Udaan (Flight)',
                'name_hindi': 'उड़ान',
                'name_romanized': 'Udaan',
                'min_age': 11,
                'max_age': 12,
                'description': 'Expert communication, creative mastery, and cultural leadership.',
                'learning_objectives': [
                    'Create sophisticated compositions',
                    'Master idiomatic expressions',
                    'Learn 400+ expert vocabulary',
                    'Lead cultural discussions',
                ],
                'peppi_welcome': 'Ready to soar with your Hindi!',
                'peppi_completion': "You're soaring high in Hindi!",
                'emoji': '🚀',
                'theme_color': '#3b82f6',
                'order': 8,
                'estimated_hours': 50,
            },
            {
                'code': 'L9',
                'name_english': 'Ratna (Gem)',
                'name_hindi': 'रत्न',
                'name_romanized': 'Ratna',
                'min_age': 12,
                'max_age': 13,
                'description': 'Professional proficiency, literary expertise, and cultural ambassador.',
                'learning_objectives': [
                    'Achieve professional fluency',
                    'Master all literary forms',
                    'Learn 450+ professional vocabulary',
                    'Serve as cultural ambassador',
                ],
                'peppi_welcome': "You're a precious gem in Hindi!",
                'peppi_completion': "You're a true Hindi gem!",
                'emoji': '💎',
                'theme_color': '#8b5cf6',
                'order': 9,
                'estimated_hours': 55,
            },
            {
                'code': 'L10',
                'name_english': 'Mukut (Crown)',
                'name_hindi': 'मुकुट',
                'name_romanized': 'Mukut',
                'min_age': 13,
                'max_age': 14,
                'description': 'Complete mastery, cultural excellence, and heritage preservation.',
                'learning_objectives': [
                    'Complete language mastery',
                    'Preserve cultural heritage',
                    'Master 500+ elite vocabulary',
                    'Mentor younger learners',
                ],
                'peppi_welcome': "You've earned your crown in Hindi!",
                'peppi_completion': "Congratulations! You're a Hindi master!",
                'emoji': '👑',
                'theme_color': '#a855f7',
                'order': 10,
                'estimated_hours': 60,
            },
        ]

        created_count = 0
        updated_count = 0

        for level_data in levels_data:
            level, created = CurriculumLevel.objects.update_or_create(
                code=level_data['code'],
                defaults=level_data
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created level {level.code}: {level.name_english}')
                )
            else:
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'Updated level {level.code}: {level.name_english}')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\nCompleted! Created: {created_count}, Updated: {updated_count}'
            )
        )
