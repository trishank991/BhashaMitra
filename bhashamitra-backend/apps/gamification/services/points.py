"""Points service."""
from django.conf import settings


class PointsService:
    """Service for calculating points."""

    @staticmethod
    def calculate_story_completion_points(level: int) -> int:
        """Calculate points for story completion."""
        return settings.POINTS_CONFIG['STORY_COMPLETED_BASE'] * level

    @staticmethod
    def calculate_page_points(pages: int) -> int:
        """Calculate points for pages read."""
        return pages * settings.POINTS_CONFIG['PAGE_READ']

    @staticmethod
    def calculate_recording_points() -> int:
        """Calculate points for voice recording."""
        return settings.POINTS_CONFIG['VOICE_RECORDING']

    @staticmethod
    def award_points(child, points: int, reason: str = None):
        """Award points to a child."""
        child.total_points += points
        child.save(update_fields=['total_points'])
        return child.total_points
