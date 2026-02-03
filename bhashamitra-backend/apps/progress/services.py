"""Progress services."""
from django.db import transaction
from django.utils import timezone
from django.conf import settings
from .models import Progress, DailyActivity


class ProgressService:
    """Service for managing progress."""

    @staticmethod
    @transaction.atomic
    def start_story(child, story) -> Progress:
        """Start or resume a story."""
        progress, created = Progress.objects.get_or_create(
            child=child,
            story=story,
            defaults={
                'status': Progress.Status.IN_PROGRESS,
                'started_at': timezone.now(),
                'last_read_at': timezone.now(),
            }
        )

        if created:
            points = settings.POINTS_CONFIG['STORY_STARTED']
            child.total_points += points
            child.save(update_fields=['total_points'])
            progress.points_earned = points
            progress.save()

            ProgressService._update_daily_activity(child, stories_started=1, points=points)

        return progress

    @staticmethod
    @transaction.atomic
    def update_progress(progress, current_page: int, time_spent: int = 0) -> Progress:
        """Update reading progress."""
        pages_read = max(0, current_page - progress.current_page)

        progress.current_page = current_page
        progress.pages_completed = current_page
        progress.time_spent_seconds += time_spent
        progress.last_read_at = timezone.now()

        if progress.status == Progress.Status.NOT_STARTED:
            progress.status = Progress.Status.IN_PROGRESS
            progress.started_at = timezone.now()

        if pages_read > 0:
            points = pages_read * settings.POINTS_CONFIG['PAGE_READ']
            progress.child.total_points += points
            progress.child.save(update_fields=['total_points'])
            progress.points_earned += points
            ProgressService._update_daily_activity(
                progress.child, pages_read=pages_read, time_spent=time_spent, points=points
            )

        progress.save()

        # Update streak
        from apps.gamification.services.streaks import StreakService
        StreakService.update_streak(progress.child)

        return progress

    @staticmethod
    @transaction.atomic
    def complete_story(progress, time_spent: int = 0) -> dict:
        """Mark story as completed."""
        remaining_pages = progress.story.page_count - progress.pages_completed
        page_points = remaining_pages * settings.POINTS_CONFIG['PAGE_READ']
        completion_points = settings.POINTS_CONFIG['STORY_COMPLETED_BASE'] * progress.story.level
        total_points = page_points + completion_points

        progress.status = Progress.Status.COMPLETED
        progress.current_page = progress.story.page_count
        progress.pages_completed = progress.story.page_count
        progress.time_spent_seconds += time_spent
        progress.completed_at = timezone.now()
        progress.points_earned += total_points
        progress.save()

        progress.child.total_points += total_points
        progress.child.save(update_fields=['total_points'])

        ProgressService._update_daily_activity(
            progress.child, stories_completed=1, pages_read=remaining_pages,
            time_spent=time_spent, points=total_points
        )

        # Update streak and check badges
        from apps.gamification.services.streaks import StreakService
        from apps.gamification.services.badges import BadgeService
        from apps.gamification.services.levels import LevelService

        StreakService.update_streak(progress.child)
        new_badges = BadgeService.check_and_award_badges(progress.child)
        level_up = LevelService.check_level_up(progress.child)

        return {
            'progress': progress,
            'points_awarded': total_points,
            'new_badges': new_badges,
            'level_up': level_up,
        }

    @staticmethod
    def _update_daily_activity(child, **kwargs):
        """Update daily activity record."""
        today = timezone.now().date()
        activity, _ = DailyActivity.objects.get_or_create(child=child, date=today)

        for field, value in kwargs.items():
            if hasattr(activity, field):
                setattr(activity, field, getattr(activity, field) + value)

        activity.save()
