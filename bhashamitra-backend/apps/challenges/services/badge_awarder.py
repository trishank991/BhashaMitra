"""Badge awarding service for challenges."""
from typing import List, Dict, Optional
from django.db import transaction, models
from django.utils import timezone

from apps.gamification.models import Badge, ChildBadge
from apps.challenges.models import ChallengeAttempt, PlayerRating
from apps.children.models import Child


class BadgeAwarder:
    """Award badges based on challenge performance."""

    CHALLENGE_CRITERIA_TYPES = [
        'CHALLENGES_COMPLETED',
        'CHALLENGES_WON',
        'CHALLENGE_WIN_STREAK',
        'PERFECT_CHALLENGES',
        'UNDERDOG_WINS',
        'GIANT_SLAYER',
        'FRIENDS_INVITED',
        'FRIENDS_CONVERTED',
        'MULTIPLAYER_GAMES',
        'RATING_ACHIEVED',
        'ACCURACY_ACHIEVED',
    ]

    def __init__(self, child: Child):
        self.child = child
        self.earned_badges = []

    def get_child_stats(self) -> Dict:
        """Get current stats for badge checking."""
        # Get all completed challenge attempts for this child
        attempts = ChallengeAttempt.objects.filter(
            participant_child=self.child,
            is_completed=True
        )

        # Basic stats
        stats = {
            'challenges_completed': attempts.count(),
            'perfect_challenges': attempts.filter(
                percentage=100.0
            ).count(),
        }

        # Get rating stats
        try:
            rating = PlayerRating.objects.get(child=self.child)
            stats.update({
                'current_rating': rating.current_rating,
                'win_streak': rating.current_win_streak,
                'best_win_streak': rating.best_win_streak,
                'underdog_wins': rating.underdog_wins,
                'giant_slayer_wins': rating.giant_slayer_wins,
                'challenges_won': rating.wins,
                'multiplayer_games': rating.total_matches,
            })
        except PlayerRating.DoesNotExist:
            stats.update({
                'current_rating': 1000,
                'win_streak': 0,
                'best_win_streak': 0,
                'underdog_wins': 0,
                'giant_slayer_wins': 0,
                'challenges_won': 0,
                'multiplayer_games': 0,
            })

        # Calculate average accuracy
        if stats['challenges_completed'] > 0:
            avg_accuracy = attempts.aggregate(avg=models.Avg('percentage'))['avg']
            stats['average_accuracy'] = round(avg_accuracy or 0, 1)
        else:
            stats['average_accuracy'] = 0

        return stats

    @transaction.atomic
    def check_and_award_badges(self, challenge_attempt: Optional[ChallengeAttempt] = None) -> List[Dict]:
        """Check all badge criteria and award any earned badges."""
        self.earned_badges = []
        stats = self.get_child_stats()

        # Get all active badges the child hasn't earned yet
        earned_badge_ids = ChildBadge.objects.filter(
            child=self.child
        ).values_list('badge_id', flat=True)

        available_badges = Badge.objects.filter(
            is_active=True,
            criteria_type__in=self.CHALLENGE_CRITERIA_TYPES
        ).exclude(id__in=earned_badge_ids)

        # Check seasonal availability
        today = timezone.now().date()
        available_badges = available_badges.filter(
            models.Q(is_seasonal=False) |
            models.Q(
                is_seasonal=True,
                available_from__lte=today,
                available_until__gte=today
            )
        )

        for badge in available_badges:
            if self._check_badge_criteria(badge, stats):
                self._award_badge(badge, challenge_attempt)

        return self.earned_badges

    def _check_badge_criteria(self, badge: Badge, stats: Dict) -> bool:
        """Check if badge criteria is met."""
        criteria_type = badge.criteria_type
        criteria_value = badge.criteria_value
        criteria_extra = badge.criteria_extra or {}

        if criteria_type == 'CHALLENGES_COMPLETED':
            return stats['challenges_completed'] >= criteria_value

        elif criteria_type == 'CHALLENGES_WON':
            return stats['challenges_won'] >= criteria_value

        elif criteria_type == 'CHALLENGE_WIN_STREAK':
            return stats['best_win_streak'] >= criteria_value

        elif criteria_type == 'PERFECT_CHALLENGES':
            return stats['perfect_challenges'] >= criteria_value

        elif criteria_type == 'UNDERDOG_WINS':
            return stats['underdog_wins'] >= criteria_value

        elif criteria_type == 'GIANT_SLAYER':
            return stats['giant_slayer_wins'] >= criteria_value

        elif criteria_type == 'RATING_ACHIEVED':
            return stats['current_rating'] >= criteria_value

        elif criteria_type == 'MULTIPLAYER_GAMES':
            return stats['multiplayer_games'] >= criteria_value

        elif criteria_type == 'ACCURACY_ACHIEVED':
            return stats['average_accuracy'] >= criteria_value

        return False

    def _award_badge(self, badge: Badge, challenge_attempt: Optional[ChallengeAttempt] = None):
        """Award a badge to the child."""
        child_badge = ChildBadge.objects.create(
            child=self.child,
            badge=badge,
        )

        badge_info = {
            'badge_id': str(badge.id),
            'badge_name': badge.name,
            'badge_icon': badge.icon,
            'badge_rarity': badge.rarity,
            'badge_category': badge.category,
            'badge_description': badge.description,
            'points_bonus': badge.points_bonus,
            'earned_at': child_badge.earned_at.isoformat(),
        }

        self.earned_badges.append(badge_info)

        # Award bonus points
        if badge.points_bonus > 0:
            self.child.total_points = (self.child.total_points or 0) + badge.points_bonus
            self.child.save(update_fields=['total_points'])
