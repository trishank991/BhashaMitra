"""
Seed educational games for L1.
Run: python manage.py seed_games
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from apps.curriculum.models import Game


GAMES_DATA = [
    # MEMORY GAMES (3)
    {
        'name': 'Letter Match',
        'description': 'Match Hindi letters with their sounds - flip cards to find matching letter pairs',
        'instructions': 'Flip cards to find matching letter pairs. Remember where each card is!',
        'game_type': 'MEMORY',
        'skill_focus': 'ALPHABET',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 180,
        'questions_per_round': 8,
        'lives': 3,
        'points_per_correct': 15,
        'bonus_completion': 50,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Word Picture Match',
        'description': 'Match Hindi words with pictures - find the picture that matches each word',
        'instructions': 'Find the picture that matches each Hindi word',
        'game_type': 'MEMORY',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 240,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 20,
        'bonus_completion': 75,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Sound Match',
        'description': 'Match sounds with letters - listen and find the matching letter',
        'instructions': 'Listen to the sound and find the matching letter',
        'game_type': 'MEMORY',
        'skill_focus': 'LISTENING',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 180,
        'questions_per_round': 8,
        'lives': 3,
        'points_per_correct': 20,
        'bonus_completion': 60,
        'is_premium': False,
        'is_active': True,
    },

    # LISTENING GAMES (2)
    {
        'name': 'Listen and Tap',
        'description': 'Listen to a word and tap the correct picture',
        'instructions': 'Peppi will say a word. Tap the picture that matches!',
        'game_type': 'LISTENING',
        'skill_focus': 'LISTENING',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 120,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 10,
        'bonus_completion': 50,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Animal Sounds Quiz',
        'description': 'Identify animals by their Hindi names from sounds',
        'instructions': 'Listen to the animal sound and select the correct Hindi name',
        'game_type': 'LISTENING',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 150,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 15,
        'bonus_completion': 60,
        'is_premium': False,
        'is_active': True,
    },

    # QUIZ GAMES (3)
    {
        'name': 'Color Quiz',
        'description': 'Identify colors in Hindi',
        'instructions': 'Select the correct Hindi word for each color',
        'game_type': 'QUIZ',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 120,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 10,
        'bonus_completion': 40,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Number Quiz',
        'description': 'Count objects and match with Hindi numbers',
        'instructions': 'Count the objects and select the correct Hindi number',
        'game_type': 'QUIZ',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 150,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 15,
        'bonus_completion': 50,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Family Quiz',
        'description': 'Identify family members in Hindi',
        'instructions': 'Match family members with their Hindi names',
        'game_type': 'QUIZ',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 120,
        'questions_per_round': 10,
        'lives': 3,
        'points_per_correct': 10,
        'bonus_completion': 40,
        'is_premium': False,
        'is_active': True,
    },

    # DRAG & DROP GAMES (2)
    {
        'name': 'Letter Order',
        'description': 'Arrange Hindi letters in correct alphabetical order',
        'instructions': 'Drag letters to arrange them in alphabetical order',
        'game_type': 'DRAGDROP',
        'skill_focus': 'ALPHABET',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 180,
        'questions_per_round': 5,
        'lives': 3,
        'points_per_correct': 25,
        'bonus_completion': 75,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Word Builder',
        'description': 'Build simple Hindi words from letters',
        'instructions': 'Drag letters to form the word shown in the picture',
        'game_type': 'BUILDER',
        'skill_focus': 'SPELLING',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 240,
        'questions_per_round': 5,
        'lives': 3,
        'points_per_correct': 30,
        'bonus_completion': 100,
        'is_premium': False,
        'is_active': True,
    },

    # SPEED GAMES (2)
    {
        'name': 'Quick Tap',
        'description': 'Tap the correct answer before time runs out',
        'instructions': 'See the word, tap the matching picture quickly!',
        'game_type': 'SPEED',
        'skill_focus': 'VOCAB',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 60,
        'questions_per_round': 15,
        'lives': 3,
        'points_per_correct': 5,
        'bonus_completion': 25,
        'is_premium': False,
        'is_active': True,
    },
    {
        'name': 'Letter Race',
        'description': 'Find letters as fast as you can',
        'instructions': 'Peppi will show a letter. Find it on the board quickly!',
        'game_type': 'SPEED',
        'skill_focus': 'ALPHABET',
        'language': 'HINDI',
        'level': 1,
        'duration_seconds': 90,
        'questions_per_round': 20,
        'lives': 3,
        'points_per_correct': 5,
        'bonus_completion': 30,
        'is_premium': False,
        'is_active': True,
    },
]


class Command(BaseCommand):
    help = 'Seed educational games for L1'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Games...\n')

        created_count = 0
        updated_count = 0

        with transaction.atomic():
            for game_data in GAMES_DATA:
                game, created = Game.objects.update_or_create(
                    name=game_data['name'],
                    language=game_data['language'],
                    defaults=game_data
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'  Created: {game.name}')
                else:
                    updated_count += 1
                    self.stdout.write(f'  Updated: {game.name}')

        self.stdout.write(self.style.SUCCESS(
            f'\nGames seeding complete! Created: {created_count}, Updated: {updated_count}'
        ))
        self.stdout.write(f'Total Games in DB: {Game.objects.count()}')
