"""Badge service."""
from django.db.models import Sum, Count
from ..models import Badge, ChildBadge


class BadgeService:
    """Service for managing badges."""

    @staticmethod
    def check_and_award_badges(child) -> list:
        """Check and award any earned badges."""
        earned_badge_ids = set(
            ChildBadge.objects.filter(child=child).values_list('badge_id', flat=True)
        )

        new_badges = []

        for badge in Badge.objects.exclude(id__in=earned_badge_ids):
            if BadgeService._check_criteria(child, badge):
                child_badge = ChildBadge.objects.create(child=child, badge=badge)
                new_badges.append(child_badge)

                # Award bonus points
                if badge.points_bonus > 0:
                    child.total_points += badge.points_bonus
                    child.save(update_fields=['total_points'])

        return new_badges

    @staticmethod
    def _check_criteria(child, badge) -> bool:
        """Check if child meets badge criteria."""
        from apps.progress.models import Progress

        if badge.criteria_type == Badge.CriteriaType.STORIES_COMPLETED:
            count = Progress.objects.filter(
                child=child, status=Progress.Status.COMPLETED
            ).count()
            return count >= badge.criteria_value

        elif badge.criteria_type == Badge.CriteriaType.STREAK_DAYS:
            from ..models import Streak
            streak = Streak.objects.filter(child=child).first()
            return streak and streak.current_streak >= badge.criteria_value

        elif badge.criteria_type == Badge.CriteriaType.POINTS_EARNED:
            return child.total_points >= badge.criteria_value

        elif badge.criteria_type == Badge.CriteriaType.VOICE_RECORDINGS:
            from ..models import VoiceRecording
            count = VoiceRecording.objects.filter(child=child).count()
            return count >= badge.criteria_value

        elif badge.criteria_type == Badge.CriteriaType.TIME_SPENT_MINUTES:
            total_seconds = Progress.objects.filter(child=child).aggregate(
                total=Sum('time_spent_seconds')
            )['total'] or 0
            return (total_seconds // 60) >= badge.criteria_value

        return False

    @staticmethod
    def get_badges_for_child(child) -> dict:
        """Get earned and available badges."""
        earned = ChildBadge.objects.filter(child=child).select_related('badge')
        all_badges = Badge.objects.all()
        earned_ids = set(cb.badge_id for cb in earned)

        return {
            'earned': [{
                'id': cb.badge.id,
                'name': cb.badge.name,
                'description': cb.badge.description,
                'icon': cb.badge.icon,
                'earned_at': cb.earned_at,
            } for cb in earned],
            'available': [{
                'id': b.id,
                'name': b.name,
                'description': b.description,
                'icon': b.icon,
                'criteria_type': b.criteria_type,
                'criteria_value': b.criteria_value,
            } for b in all_badges if b.id not in earned_ids],
        }
