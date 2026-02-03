"""Level service."""
from django.conf import settings


class LevelService:
    """Service for managing levels."""

    @staticmethod
    def calculate_level(total_points: int) -> int:
        """Calculate level based on total points."""
        thresholds = settings.LEVEL_THRESHOLDS
        level = 1

        for lvl, threshold in sorted(thresholds.items()):
            if total_points >= threshold:
                level = lvl
            else:
                break

        return level

    @staticmethod
    def check_level_up(child) -> dict:
        """Check if child leveled up."""
        current_level = child.level
        new_level = LevelService.calculate_level(child.total_points)

        if new_level > current_level:
            child.level = new_level
            child.save(update_fields=['level'])
            return {
                'leveled_up': True,
                'old_level': current_level,
                'new_level': new_level,
            }

        return {'leveled_up': False}

    @staticmethod
    def get_level_progress(child) -> dict:
        """Get level progress information."""
        thresholds = settings.LEVEL_THRESHOLDS
        current_threshold = thresholds.get(child.level, 0)
        next_threshold = thresholds.get(child.level + 1)

        if next_threshold:
            points_in_level = child.total_points - current_threshold
            points_needed = next_threshold - current_threshold
            progress_percent = int((points_in_level / points_needed) * 100)
        else:
            points_in_level = child.total_points - current_threshold
            points_needed = None
            progress_percent = 100

        return {
            'current_level': child.level,
            'total_points': child.total_points,
            'points_in_level': points_in_level,
            'points_to_next': points_needed,
            'progress_percent': progress_percent,
        }
