"""Seed badges for gamification."""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.gamification.models import Badge


BADGES = [
    # Story completion badges
    {
        'name': 'First Story',
        'description': 'Complete your first story!',
        'icon': 'book-open',
        'criteria_type': 'STORIES_COMPLETED',
        'criteria_value': 1,
        'display_order': 1,
        'points_bonus': 25,
    },
    {
        'name': 'Story Explorer',
        'description': 'Complete 5 stories',
        'icon': 'book-marked',
        'criteria_type': 'STORIES_COMPLETED',
        'criteria_value': 5,
        'display_order': 2,
        'points_bonus': 50,
    },
    {
        'name': 'Bookworm',
        'description': 'Complete 10 stories',
        'icon': 'library',
        'criteria_type': 'STORIES_COMPLETED',
        'criteria_value': 10,
        'display_order': 3,
        'points_bonus': 100,
    },
    {
        'name': 'Story Master',
        'description': 'Complete 25 stories',
        'icon': 'crown',
        'criteria_type': 'STORIES_COMPLETED',
        'criteria_value': 25,
        'display_order': 4,
        'points_bonus': 250,
    },
    # Streak badges
    {
        'name': 'Getting Started',
        'description': 'Practice 3 days in a row',
        'icon': 'flame',
        'criteria_type': 'STREAK_DAYS',
        'criteria_value': 3,
        'display_order': 10,
        'points_bonus': 30,
    },
    {
        'name': 'Week Warrior',
        'description': 'Practice 7 days in a row',
        'icon': 'fire',
        'criteria_type': 'STREAK_DAYS',
        'criteria_value': 7,
        'display_order': 11,
        'points_bonus': 70,
    },
    {
        'name': 'Fortnight Fighter',
        'description': 'Practice 14 days in a row',
        'icon': 'zap',
        'criteria_type': 'STREAK_DAYS',
        'criteria_value': 14,
        'display_order': 12,
        'points_bonus': 150,
    },
    {
        'name': 'Month Master',
        'description': 'Practice 30 days in a row',
        'icon': 'trophy',
        'criteria_type': 'STREAK_DAYS',
        'criteria_value': 30,
        'display_order': 13,
        'points_bonus': 300,
    },
    # Voice recording badges
    {
        'name': 'First Words',
        'description': 'Record your first voice recording',
        'icon': 'mic',
        'criteria_type': 'VOICE_RECORDINGS',
        'criteria_value': 1,
        'display_order': 20,
        'points_bonus': 20,
    },
    {
        'name': 'Voice Star',
        'description': 'Make 10 voice recordings',
        'icon': 'mic-vocal',
        'criteria_type': 'VOICE_RECORDINGS',
        'criteria_value': 10,
        'display_order': 21,
        'points_bonus': 100,
    },
    # Points badges
    {
        'name': 'Point Collector',
        'description': 'Earn 100 points',
        'icon': 'coins',
        'criteria_type': 'POINTS_EARNED',
        'criteria_value': 100,
        'display_order': 30,
        'points_bonus': 10,
    },
    {
        'name': 'Point Hunter',
        'description': 'Earn 500 points',
        'icon': 'gem',
        'criteria_type': 'POINTS_EARNED',
        'criteria_value': 500,
        'display_order': 31,
        'points_bonus': 50,
    },
    {
        'name': 'Point Champion',
        'description': 'Earn 1000 points',
        'icon': 'diamond',
        'criteria_type': 'POINTS_EARNED',
        'criteria_value': 1000,
        'display_order': 32,
        'points_bonus': 100,
    },
    {
        'name': 'Point Legend',
        'description': 'Earn 5000 points',
        'icon': 'sparkles',
        'criteria_type': 'POINTS_EARNED',
        'criteria_value': 5000,
        'display_order': 33,
        'points_bonus': 500,
    },
]


def seed_badges():
    """Seed all badges."""
    created_count = 0
    updated_count = 0

    for badge_data in BADGES:
        badge, created = Badge.objects.update_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"Badges: {created_count} created, {updated_count} updated. Total: {len(BADGES)}")
    return len(BADGES)


if __name__ == '__main__':
    seed_badges()
