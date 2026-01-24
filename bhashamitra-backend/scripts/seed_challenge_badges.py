"""Seed challenge-related badges for competitive play."""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.gamification.models import Badge


CHALLENGE_BADGES = [
    # Challenge Completion Badges (ACHIEVEMENT category)
    {
        'name': 'First Challenge',
        'description': 'Complete your first challenge!',
        'icon': 'swords',
        'criteria_type': 'CHALLENGES_COMPLETED',
        'criteria_value': 1,
        'display_order': 100,
        'points_bonus': 25,
        'category': 'ACHIEVEMENT',
        'rarity': 'COMMON',
    },
    {
        'name': 'Challenge Novice',
        'description': 'Complete 5 challenges',
        'icon': 'shield',
        'criteria_type': 'CHALLENGES_COMPLETED',
        'criteria_value': 5,
        'display_order': 101,
        'points_bonus': 50,
        'category': 'ACHIEVEMENT',
        'rarity': 'COMMON',
    },
    {
        'name': 'Challenge Enthusiast',
        'description': 'Complete 25 challenges',
        'icon': 'shield-check',
        'criteria_type': 'CHALLENGES_COMPLETED',
        'criteria_value': 25,
        'display_order': 102,
        'points_bonus': 150,
        'category': 'ACHIEVEMENT',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Challenge Veteran',
        'description': 'Complete 50 challenges',
        'icon': 'shield-half',
        'criteria_type': 'CHALLENGES_COMPLETED',
        'criteria_value': 50,
        'display_order': 103,
        'points_bonus': 300,
        'category': 'ACHIEVEMENT',
        'rarity': 'RARE',
    },
    {
        'name': 'Challenge Master',
        'description': 'Complete 100 challenges',
        'icon': 'castle',
        'criteria_type': 'CHALLENGES_COMPLETED',
        'criteria_value': 100,
        'display_order': 104,
        'points_bonus': 500,
        'category': 'ACHIEVEMENT',
        'rarity': 'EPIC',
    },

    # Win Badges (SKILL category)
    {
        'name': 'First Victory',
        'description': 'Win your first challenge!',
        'icon': 'medal',
        'criteria_type': 'CHALLENGES_WON',
        'criteria_value': 1,
        'display_order': 110,
        'points_bonus': 30,
        'category': 'SKILL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Rising Competitor',
        'description': 'Win 10 challenges',
        'icon': 'award',
        'criteria_type': 'CHALLENGES_WON',
        'criteria_value': 10,
        'display_order': 111,
        'points_bonus': 100,
        'category': 'SKILL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Skilled Competitor',
        'description': 'Win 25 challenges',
        'icon': 'trophy',
        'criteria_type': 'CHALLENGES_WON',
        'criteria_value': 25,
        'display_order': 112,
        'points_bonus': 250,
        'category': 'SKILL',
        'rarity': 'RARE',
    },
    {
        'name': 'Champion',
        'description': 'Win 50 challenges',
        'icon': 'crown',
        'criteria_type': 'CHALLENGES_WON',
        'criteria_value': 50,
        'display_order': 113,
        'points_bonus': 500,
        'category': 'SKILL',
        'rarity': 'EPIC',
    },
    {
        'name': 'Legend',
        'description': 'Win 100 challenges',
        'icon': 'sparkles',
        'criteria_type': 'CHALLENGES_WON',
        'criteria_value': 100,
        'display_order': 114,
        'points_bonus': 1000,
        'category': 'SKILL',
        'rarity': 'LEGENDARY',
    },

    # Win Streak Badges (STREAK category)
    {
        'name': 'On a Roll',
        'description': 'Win 3 challenges in a row',
        'icon': 'flame',
        'criteria_type': 'CHALLENGE_WIN_STREAK',
        'criteria_value': 3,
        'display_order': 120,
        'points_bonus': 50,
        'category': 'STREAK',
        'rarity': 'COMMON',
    },
    {
        'name': 'Hot Streak',
        'description': 'Win 5 challenges in a row',
        'icon': 'fire',
        'criteria_type': 'CHALLENGE_WIN_STREAK',
        'criteria_value': 5,
        'display_order': 121,
        'points_bonus': 100,
        'category': 'STREAK',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Unstoppable',
        'description': 'Win 10 challenges in a row',
        'icon': 'zap',
        'criteria_type': 'CHALLENGE_WIN_STREAK',
        'criteria_value': 10,
        'display_order': 122,
        'points_bonus': 250,
        'category': 'STREAK',
        'rarity': 'RARE',
    },
    {
        'name': 'Invincible',
        'description': 'Win 15 challenges in a row',
        'icon': 'infinity',
        'criteria_type': 'CHALLENGE_WIN_STREAK',
        'criteria_value': 15,
        'display_order': 123,
        'points_bonus': 500,
        'category': 'STREAK',
        'rarity': 'LEGENDARY',
    },

    # Perfect Challenge Badges (SKILL category)
    {
        'name': 'Perfect Start',
        'description': 'Get 100% on your first challenge',
        'icon': 'check-circle',
        'criteria_type': 'PERFECT_CHALLENGES',
        'criteria_value': 1,
        'display_order': 130,
        'points_bonus': 50,
        'category': 'SKILL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Perfectionist',
        'description': 'Get 100% on 5 challenges',
        'icon': 'badge-check',
        'criteria_type': 'PERFECT_CHALLENGES',
        'criteria_value': 5,
        'display_order': 131,
        'points_bonus': 150,
        'category': 'SKILL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Flawless',
        'description': 'Get 100% on 10 challenges',
        'icon': 'star',
        'criteria_type': 'PERFECT_CHALLENGES',
        'criteria_value': 10,
        'display_order': 132,
        'points_bonus': 300,
        'category': 'SKILL',
        'rarity': 'RARE',
    },
    {
        'name': 'Perfect Master',
        'description': 'Get 100% on 25 challenges',
        'icon': 'gem',
        'criteria_type': 'PERFECT_CHALLENGES',
        'criteria_value': 25,
        'display_order': 133,
        'points_bonus': 750,
        'category': 'SKILL',
        'rarity': 'LEGENDARY',
    },

    # Underdog Badges (SPECIAL category)
    {
        'name': 'Underdog',
        'description': 'Beat someone with a higher rating',
        'icon': 'dog',
        'criteria_type': 'UNDERDOG_WINS',
        'criteria_value': 1,
        'display_order': 140,
        'points_bonus': 40,
        'category': 'SPECIAL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Comeback Kid',
        'description': 'Beat 5 higher-rated opponents',
        'icon': 'rocket',
        'criteria_type': 'UNDERDOG_WINS',
        'criteria_value': 5,
        'display_order': 141,
        'points_bonus': 150,
        'category': 'SPECIAL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Giant Slayer',
        'description': 'Beat someone 200+ rating above you',
        'icon': 'sword',
        'criteria_type': 'GIANT_SLAYER',
        'criteria_value': 1,
        'display_order': 142,
        'points_bonus': 200,
        'category': 'SPECIAL',
        'rarity': 'RARE',
    },
    {
        'name': 'Giant Hunter',
        'description': 'Giant slayer 5 times',
        'icon': 'axe',
        'criteria_type': 'GIANT_SLAYER',
        'criteria_value': 5,
        'display_order': 143,
        'points_bonus': 500,
        'category': 'SPECIAL',
        'rarity': 'EPIC',
    },

    # Rating Badges (SKILL category)
    {
        'name': 'Rising Star',
        'description': 'Reach 1100 rating',
        'icon': 'trending-up',
        'criteria_type': 'RATING_ACHIEVED',
        'criteria_value': 1100,
        'display_order': 150,
        'points_bonus': 50,
        'category': 'SKILL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Challenger',
        'description': 'Reach 1200 rating',
        'icon': 'target',
        'criteria_type': 'RATING_ACHIEVED',
        'criteria_value': 1200,
        'display_order': 151,
        'points_bonus': 100,
        'category': 'SKILL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Competitor',
        'description': 'Reach 1300 rating',
        'icon': 'circle-dot',
        'criteria_type': 'RATING_ACHIEVED',
        'criteria_value': 1300,
        'display_order': 152,
        'points_bonus': 200,
        'category': 'SKILL',
        'rarity': 'RARE',
    },
    {
        'name': 'Expert',
        'description': 'Reach 1500 rating',
        'icon': 'brain',
        'criteria_type': 'RATING_ACHIEVED',
        'criteria_value': 1500,
        'display_order': 153,
        'points_bonus': 400,
        'category': 'SKILL',
        'rarity': 'EPIC',
    },
    {
        'name': 'Grandmaster',
        'description': 'Reach 1800 rating',
        'icon': 'graduation-cap',
        'criteria_type': 'RATING_ACHIEVED',
        'criteria_value': 1800,
        'display_order': 154,
        'points_bonus': 1000,
        'category': 'SKILL',
        'rarity': 'LEGENDARY',
    },

    # Multiplayer Badges (SOCIAL category)
    {
        'name': 'Social Learner',
        'description': 'Play 5 multiplayer games',
        'icon': 'users',
        'criteria_type': 'MULTIPLAYER_GAMES',
        'criteria_value': 5,
        'display_order': 160,
        'points_bonus': 30,
        'category': 'SOCIAL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Team Player',
        'description': 'Play 25 multiplayer games',
        'icon': 'users-2',
        'criteria_type': 'MULTIPLAYER_GAMES',
        'criteria_value': 25,
        'display_order': 161,
        'points_bonus': 100,
        'category': 'SOCIAL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Community Champion',
        'description': 'Play 100 multiplayer games',
        'icon': 'globe',
        'criteria_type': 'MULTIPLAYER_GAMES',
        'criteria_value': 100,
        'display_order': 162,
        'points_bonus': 300,
        'category': 'SOCIAL',
        'rarity': 'RARE',
    },

    # Accuracy Badges (SKILL category)
    {
        'name': 'Accurate',
        'description': 'Maintain 70% accuracy across challenges',
        'icon': 'crosshair',
        'criteria_type': 'ACCURACY_ACHIEVED',
        'criteria_value': 70,
        'display_order': 170,
        'points_bonus': 50,
        'category': 'SKILL',
        'rarity': 'COMMON',
    },
    {
        'name': 'Sharp Mind',
        'description': 'Maintain 80% accuracy across challenges',
        'icon': 'bullseye',
        'criteria_type': 'ACCURACY_ACHIEVED',
        'criteria_value': 80,
        'display_order': 171,
        'points_bonus': 150,
        'category': 'SKILL',
        'rarity': 'UNCOMMON',
    },
    {
        'name': 'Precision Expert',
        'description': 'Maintain 90% accuracy across challenges',
        'icon': 'focus',
        'criteria_type': 'ACCURACY_ACHIEVED',
        'criteria_value': 90,
        'display_order': 172,
        'points_bonus': 400,
        'category': 'SKILL',
        'rarity': 'EPIC',
    },
]


def seed_challenge_badges():
    """Seed all challenge badges."""
    created_count = 0
    updated_count = 0

    for badge_data in CHALLENGE_BADGES:
        badge, created = Badge.objects.update_or_create(
            name=badge_data['name'],
            defaults=badge_data
        )
        if created:
            created_count += 1
            print(f"  Created: {badge_data['name']} ({badge_data['rarity']})")
        else:
            updated_count += 1
            print(f"  Updated: {badge_data['name']}")

    print(f"\nChallenge Badges: {created_count} created, {updated_count} updated. Total: {len(CHALLENGE_BADGES)}")
    return len(CHALLENGE_BADGES)


if __name__ == '__main__':
    print("Seeding challenge badges...")
    seed_challenge_badges()
    print("\nDone!")
