"""Streak service."""
from django.utils import timezone
from datetime import timedelta
from ..models import Streak


class StreakService:
    """Service for managing streaks."""

    @staticmethod
    def update_streak(child) -> Streak:
        """Update streak based on activity."""
        streak, created = Streak.objects.get_or_create(child=child)
        today = timezone.now().date()

        if created or streak.last_activity_date is None:
            streak.current_streak = 1
            streak.longest_streak = 1
            streak.last_activity_date = today
        elif streak.last_activity_date == today:
            # Already active today, no change
            pass
        elif streak.last_activity_date == today - timedelta(days=1):
            # Consecutive day
            streak.current_streak += 1
            streak.longest_streak = max(streak.longest_streak, streak.current_streak)
            streak.last_activity_date = today
        else:
            # Streak broken
            streak.current_streak = 1
            streak.last_activity_date = today

        streak.save()
        return streak

    @staticmethod
    def get_streak(child) -> dict:
        """Get streak information."""
        streak, _ = Streak.objects.get_or_create(child=child)
        today = timezone.now().date()

        is_active = (
            streak.last_activity_date == today or
            streak.last_activity_date == today - timedelta(days=1)
        )

        return {
            'current_streak': streak.current_streak,
            'longest_streak': streak.longest_streak,
            'last_activity_date': streak.last_activity_date,
            'is_active': is_active,
        }
