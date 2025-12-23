"""
Seed sample progress data for testing parent dashboard.

Usage:
    python manage.py seed_parent_dashboard_data
    python manage.py seed_parent_dashboard_data --days 30
"""
import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.speech.models import PeppiMimicAttempt, PeppiMimicChallenge


class Command(BaseCommand):
    help = 'Seed sample progress data for parent dashboard testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Number of days of data to generate (default: 30)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing progress data first'
        )

    def handle(self, *args, **options):
        days = options['days']
        clear = options['clear']

        if clear:
            self.stdout.write('Clearing existing progress data...')
            DailyProgress.objects.all().delete()
            ActivityLog.objects.all().delete()
            PeppiMimicAttempt.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Cleared existing data'))

        children = Child.objects.filter(deleted_at__isnull=True)

        if not children.exists():
            self.stdout.write(self.style.ERROR('No children found in database'))
            return

        self.stdout.write(f'Seeding {days} days of data for {children.count()} children...')

        today = timezone.now().date()

        for child in children:
            self.seed_child_data(child, days, today)

        self.stdout.write(self.style.SUCCESS(
            f'Successfully seeded progress data for {children.count()} children'
        ))

    def seed_child_data(self, child, days, today):
        """Seed progress data for a single child."""
        self.stdout.write(f'  Seeding data for {child.name}...')

        # Activity types for activity log
        activity_types = [
            ('LESSON_COMPLETED', 'Completed lesson: {}', ['Alphabets', 'Numbers', 'Colors', 'Animals', 'Family']),
            ('STORY_READ', 'Read story: {}', ['The Clever Crow', 'Moon and Stars', 'Rainbow Fish', 'Little Peppi']),
            ('GAME_COMPLETED', 'Played game: {}', ['Letter Match', 'Word Builder', 'Memory Cards', 'Pronunciation Practice']),
            ('WORD_LEARNED', 'Learned new word: {}', ['Namaste', 'Dhanyavaad', 'Pyaar', 'Khush', 'Dost']),
            ('BADGE_EARNED', 'Earned badge: {}', ['First Steps', 'Word Master', 'Story Lover', 'Streak Hero']),
        ]

        # Peppi practice phrases (Hindi words with romanization and meaning)
        peppi_phrases = [
            {'word': 'नमस्ते', 'romanization': 'namaste', 'meaning': 'Hello/Greetings'},
            {'word': 'धन्यवाद', 'romanization': 'dhanyavaad', 'meaning': 'Thank you'},
            {'word': 'कैसे हो', 'romanization': 'kaise ho', 'meaning': 'How are you?'},
            {'word': 'मेरा नाम', 'romanization': 'mera naam', 'meaning': 'My name'},
            {'word': 'बहुत अच्छा', 'romanization': 'bahut accha', 'meaning': 'Very good'},
            {'word': 'एक दो तीन', 'romanization': 'ek do teen', 'meaning': 'One two three'},
            {'word': 'लाल', 'romanization': 'laal', 'meaning': 'Red'},
            {'word': 'पीला', 'romanization': 'peela', 'meaning': 'Yellow'},
            {'word': 'नीला', 'romanization': 'neela', 'meaning': 'Blue'},
            {'word': 'माँ', 'romanization': 'maa', 'meaning': 'Mother'},
            {'word': 'पापा', 'romanization': 'papa', 'meaning': 'Father'},
            {'word': 'पानी', 'romanization': 'paani', 'meaning': 'Water'},
            {'word': 'खाना', 'romanization': 'khaana', 'meaning': 'Food'},
        ]

        # Seed daily progress for each day
        for day_offset in range(days):
            date = today - timedelta(days=day_offset)

            # Random chance of activity (80% on weekdays, 60% on weekends)
            is_weekend = date.weekday() >= 5
            activity_chance = 0.6 if is_weekend else 0.8

            if random.random() > activity_chance:
                continue  # Skip this day

            # Generate daily progress
            time_spent = random.randint(10, 45)  # 10-45 minutes
            lessons = random.randint(1, 4)
            exercises = random.randint(0, 3)
            games = random.randint(0, 2)
            points = (lessons * 10) + (exercises * 5) + (games * 8) + random.randint(0, 20)

            DailyProgress.objects.update_or_create(
                child=child,
                date=date,
                defaults={
                    'time_spent_minutes': time_spent,
                    'lessons_completed': lessons,
                    'exercises_completed': exercises,
                    'games_played': games,
                    'points_earned': points,
                }
            )

            # Create activity log entries for this day
            num_activities = random.randint(2, 5)
            for _ in range(num_activities):
                activity_type, template, options = random.choice(activity_types)
                description = template.format(random.choice(options))

                # Create activity at random time during the day
                activity_time = timezone.make_aware(
                    timezone.datetime(
                        date.year, date.month, date.day,
                        random.randint(9, 20),  # 9am to 8pm
                        random.randint(0, 59)
                    )
                )

                ActivityLog.objects.create(
                    child=child,
                    activity_type=activity_type,
                    description=description,
                    points_earned=random.randint(5, 20),
                    created_at=activity_time,
                )

            # Create Peppi pronunciation attempts (some days)
            if random.random() > 0.5:
                num_attempts = random.randint(1, 3)
                for _ in range(num_attempts):
                    phrase_data = random.choice(peppi_phrases)

                    # Get or create a challenge
                    challenge, _ = PeppiMimicChallenge.objects.get_or_create(
                        word=phrase_data['word'],
                        language='HINDI',
                        defaults={
                            'romanization': phrase_data['romanization'],
                            'meaning': phrase_data['meaning'],
                            'difficulty': random.choice([1, 2, 3]),  # 1=Easy, 2=Medium, 3=Hard
                            'category': random.choice(['GREETING', 'FAMILY', 'DAILY', 'NUMBERS']),
                            'points_reward': random.choice([5, 10, 15]),
                        }
                    )

                    # Create attempt with realistic score distribution
                    # Most attempts should be 60-95% (learning curve)
                    final_score = max(40, min(100, int(random.gauss(75, 15))))
                    stars = 3 if final_score >= 85 else (2 if final_score >= 65 else (1 if final_score >= 45 else 0))

                    attempt_time = timezone.make_aware(
                        timezone.datetime(
                            date.year, date.month, date.day,
                            random.randint(9, 20),
                            random.randint(0, 59)
                        )
                    )

                    PeppiMimicAttempt.objects.create(
                        child=child,
                        challenge=challenge,
                        audio_url=f"https://example.com/recordings/{child.id}/{challenge.id}.webm",
                        duration_ms=random.randint(500, 2000),
                        stt_transcription=phrase_data['word'],
                        stt_confidence=random.uniform(0.7, 0.99),
                        text_match_score=final_score * random.uniform(0.9, 1.1),
                        final_score=final_score,
                        stars=stars,
                        audio_energy_score=random.uniform(60, 95),
                        duration_match_score=random.uniform(70, 100),
                        created_at=attempt_time,
                    )

        self.stdout.write(f'    Created data for {child.name}')

    def _get_feedback(self, score):
        """Get appropriate feedback based on score."""
        if score >= 90:
            return random.choice([
                'Perfect pronunciation!',
                'Excellent! You sound like a native speaker!',
                'Outstanding! Keep it up!',
            ])
        elif score >= 75:
            return random.choice([
                'Great job! Almost perfect!',
                'Very good! Just a little more practice.',
                'Well done! You are improving fast!',
            ])
        elif score >= 60:
            return random.choice([
                'Good effort! Keep practicing.',
                'Nice try! Listen carefully and try again.',
                'You are learning! Practice makes perfect.',
            ])
        else:
            return random.choice([
                'Keep trying! You can do it!',
                'Listen to Peppi and try again.',
                'Practice slowly and clearly.',
            ])
