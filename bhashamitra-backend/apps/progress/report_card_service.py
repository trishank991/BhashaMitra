"""
Report Card Service for BhashaMitra.

Generates comprehensive learning reports by aggregating data from:
- Progress tracking (stories, lessons completed)
- Gamification (points, achievements, streaks)
- Curriculum (vocabulary, level progress)
- Speech (pronunciation practice, mimic challenges)
"""

from datetime import date, timedelta
from typing import Optional, Dict, List, Any
import logging
from django.db.models import Sum, Count, Avg, Max, F
from django.utils import timezone

logger = logging.getLogger(__name__)


class ReportCardService:
    """
    Service for generating comprehensive child learning reports.

    Report Types:
    - Comprehensive: Full overview for parents
    - Skills Breakdown: Detailed skill-by-skill analysis
    - Monthly Stats: Monthly comparison data
    """

    @classmethod
    def get_comprehensive_report(
        cls,
        child_id: str,
        period_days: int = 30
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive report card for a child.

        Args:
            child_id: UUID of the child
            period_days: Number of days to include in report (default 30)

        Returns:
            Complete report card data
        """
        from apps.children.models import Child
        from apps.progress.models import Progress, DailyProgress, ActivityLog

        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return {'error': 'Child not found'}

        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=period_days)

        # Aggregate overall stats
        overall_stats = cls._get_overall_stats(child, start_date, end_date)

        # Get skill mastery breakdown
        skill_mastery = cls._get_skill_mastery(child)

        # Get content completion stats
        content_completion = cls._get_content_completion(child, start_date, end_date)

        # Get achievements and badges
        achievements = cls._get_achievements(child, start_date, end_date)

        # Get pronunciation practice stats
        pronunciation_stats = cls._get_pronunciation_stats(child, start_date, end_date)

        # Calculate streak information
        streak_info = cls._get_streak_info(child)

        # Generate insights and recommendations
        insights = cls._generate_insights(child, overall_stats, skill_mastery)

        return {
            'child': {
                'id': str(child.id),
                'name': child.name,
                'age': cls._calculate_age(child.date_of_birth),
                'language': child.language,
                'level': child.level,
                'total_points': child.total_points,
            },
            'report_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': period_days,
            },
            'overall_stats': overall_stats,
            'skill_mastery': skill_mastery,
            'content_completion': content_completion,
            'achievements': achievements,
            'pronunciation': pronunciation_stats,
            'streak': streak_info,
            'insights': insights,
            'generated_at': timezone.now().isoformat(),
        }

    @classmethod
    def _get_overall_stats(cls, child, start_date, end_date) -> Dict[str, Any]:
        """Calculate overall learning statistics."""
        from apps.progress.models import DailyProgress

        daily_progress = DailyProgress.objects.filter(
            child=child,
            date__gte=start_date,
            date__lte=end_date
        )

        totals = daily_progress.aggregate(
            total_time=Sum('time_spent_minutes'),
            total_lessons=Sum('lessons_completed'),
            total_exercises=Sum('exercises_completed'),
            total_games=Sum('games_played'),
            total_points=Sum('points_earned'),
        )

        days_active = daily_progress.filter(time_spent_minutes__gt=0).count()
        total_days = (end_date - start_date).days + 1

        return {
            'total_time_minutes': totals['total_time'] or 0,
            'total_time_hours': round((totals['total_time'] or 0) / 60, 1),
            'lessons_completed': totals['total_lessons'] or 0,
            'exercises_completed': totals['total_exercises'] or 0,
            'games_played': totals['total_games'] or 0,
            'points_earned': totals['total_points'] or 0,
            'days_active': days_active,
            'total_days': total_days,
            'engagement_rate': round((days_active / total_days) * 100, 1) if total_days > 0 else 0,
            'avg_time_per_day': round((totals['total_time'] or 0) / max(days_active, 1), 1),
        }

    @classmethod
    def _get_skill_mastery(cls, child) -> List[Dict[str, Any]]:
        """Get detailed skill mastery breakdown."""
        skills = []

        # Vocabulary mastery (from SRS flashcards)
        try:
            from apps.curriculum.models.vocabulary import WordProgress
            word_progress = WordProgress.objects.filter(child=child)
            total_words = word_progress.count()
            mastered_words = word_progress.filter(mastered=True).count()

            if total_words > 0:
                skills.append({
                    'skill': 'Vocabulary',
                    'icon': '📚',
                    'total': total_words,
                    'mastered': mastered_words,
                    'percentage': round((mastered_words / total_words) * 100, 1),
                    'level': cls._get_mastery_level(mastered_words / total_words),
                })
        except Exception:
            pass

        # Pronunciation mastery (from Peppi Mimic)
        try:
            from apps.speech.models import PeppiMimicProgress
            mimic_progress = PeppiMimicProgress.objects.filter(child=child)
            total_challenges = mimic_progress.count()
            mastered_challenges = mimic_progress.filter(mastered=True).count()

            if total_challenges > 0:
                skills.append({
                    'skill': 'Pronunciation',
                    'icon': '🎤',
                    'total': total_challenges,
                    'mastered': mastered_challenges,
                    'percentage': round((mastered_challenges / total_challenges) * 100, 1),
                    'level': cls._get_mastery_level(mastered_challenges / total_challenges),
                })
        except Exception:
            pass

        # Story Reading (from Progress)
        try:
            from apps.progress.models import Progress
            story_progress = Progress.objects.filter(child=child)
            total_stories = story_progress.count()
            completed_stories = story_progress.filter(status='COMPLETED').count()

            if total_stories > 0:
                skills.append({
                    'skill': 'Reading',
                    'icon': '📖',
                    'total': total_stories,
                    'mastered': completed_stories,
                    'percentage': round((completed_stories / total_stories) * 100, 1),
                    'level': cls._get_mastery_level(completed_stories / total_stories),
                })
        except Exception:
            pass

        # Game Performance
        try:
            from apps.curriculum.models.games import GameSession
            game_sessions = GameSession.objects.filter(child=child, completed=True)
            total_games = game_sessions.count()

            if total_games > 0:
                avg_score = game_sessions.aggregate(avg=Avg('score'))['avg'] or 0
                skills.append({
                    'skill': 'Games',
                    'icon': '🎮',
                    'total': total_games,
                    'avg_score': round(avg_score, 1),
                    'percentage': min(100, round(avg_score, 1)),
                    'level': cls._get_mastery_level(avg_score / 100),
                })
        except Exception:
            pass

        return skills

    @classmethod
    def _get_content_completion(cls, child, start_date, end_date) -> Dict[str, Any]:
        """Get content completion statistics."""
        from apps.progress.models import Progress

        # Story completion in period
        story_stats = Progress.objects.filter(
            child=child,
            completed_at__gte=start_date,
            completed_at__lte=end_date
        ).aggregate(
            completed=Count('id', filter=F('status') == 'COMPLETED'),
            in_progress=Count('id', filter=F('status') == 'IN_PROGRESS'),
            total_pages=Sum('pages_completed'),
        )

        # Lesson progress (from curriculum)
        lesson_stats = {'completed': 0, 'total': 0}
        try:
            from apps.curriculum.models.progress import LessonProgress
            lesson_progress = LessonProgress.objects.filter(child=child)
            lesson_stats = {
                'completed': lesson_progress.filter(completed=True).count(),
                'total': lesson_progress.count(),
            }
        except Exception:
            pass

        return {
            'stories': {
                'completed_in_period': story_stats['completed'] or 0,
                'in_progress': story_stats['in_progress'] or 0,
                'pages_read': story_stats['total_pages'] or 0,
            },
            'lessons': lesson_stats,
        }

    @classmethod
    def _get_achievements(cls, child, start_date, end_date) -> Dict[str, Any]:
        """Get achievements and badges earned."""
        from apps.progress.models import ActivityLog

        achievements = ActivityLog.objects.filter(
            child=child,
            created_at__gte=start_date,
            created_at__lte=end_date
        )

        badges_earned = achievements.filter(activity_type='BADGE_EARNED').count()
        level_ups = achievements.filter(activity_type='LEVEL_UP').count()
        streak_milestones = achievements.filter(activity_type='STREAK_MILESTONE').count()

        # Get recent achievements
        recent = achievements.filter(
            activity_type__in=['BADGE_EARNED', 'LEVEL_UP', 'STREAK_MILESTONE']
        ).order_by('-created_at')[:5]

        recent_list = []
        for achievement in recent:
            recent_list.append({
                'type': achievement.activity_type,
                'description': achievement.description,
                'points': achievement.points_earned,
                'date': achievement.created_at.isoformat(),
            })

        return {
            'badges_earned': badges_earned,
            'level_ups': level_ups,
            'streak_milestones': streak_milestones,
            'total': badges_earned + level_ups + streak_milestones,
            'recent': recent_list,
        }

    @classmethod
    def _get_pronunciation_stats(cls, child, start_date, end_date) -> Dict[str, Any]:
        """Get pronunciation practice statistics."""
        try:
            from apps.speech.models import PeppiMimicAttempt, PeppiMimicProgress

            attempts = PeppiMimicAttempt.objects.filter(
                child=child,
                created_at__gte=start_date,
                created_at__lte=end_date
            )

            totals = attempts.aggregate(
                total_attempts=Count('id'),
                avg_score=Avg('final_score'),
                total_stars=Sum('stars'),
                perfect_count=Count('id', filter=F('stars') == 3),
            )

            mastered = PeppiMimicProgress.objects.filter(
                child=child,
                mastered=True
            ).count()

            return {
                'total_attempts': totals['total_attempts'] or 0,
                'average_score': round(totals['avg_score'] or 0, 1),
                'total_stars': totals['total_stars'] or 0,
                'perfect_scores': totals['perfect_count'] or 0,
                'words_mastered': mastered,
            }
        except Exception:
            return {
                'total_attempts': 0,
                'average_score': 0,
                'total_stars': 0,
                'perfect_scores': 0,
                'words_mastered': 0,
            }

    @classmethod
    def _get_streak_info(cls, child) -> Dict[str, Any]:
        """Calculate streak information."""
        from apps.progress.models import DailyProgress

        today = timezone.now().date()
        current_streak = 0
        longest_streak = 0
        temp_streak = 0
        current_date = today

        # Calculate current streak
        while True:
            has_activity = DailyProgress.objects.filter(
                child=child,
                date=current_date,
                time_spent_minutes__gt=0
            ).exists()

            if has_activity:
                current_streak += 1
                current_date -= timedelta(days=1)
            else:
                break

            if current_streak >= 365:
                break

        # Calculate longest streak (look back 90 days)
        progress_days = DailyProgress.objects.filter(
            child=child,
            date__gte=today - timedelta(days=90),
            time_spent_minutes__gt=0
        ).values_list('date', flat=True).order_by('date')

        prev_date = None
        for d in progress_days:
            if prev_date is None or (d - prev_date).days == 1:
                temp_streak += 1
            else:
                longest_streak = max(longest_streak, temp_streak)
                temp_streak = 1
            prev_date = d

        longest_streak = max(longest_streak, temp_streak)

        return {
            'current_streak': current_streak,
            'longest_streak': longest_streak,
            'streak_status': cls._get_streak_status(current_streak),
        }

    @classmethod
    def _generate_insights(
        cls,
        child,
        overall_stats: Dict,
        skill_mastery: List
    ) -> List[Dict[str, Any]]:
        """Generate personalized insights and recommendations."""
        insights = []

        # Engagement insight
        engagement = overall_stats.get('engagement_rate', 0)
        if engagement >= 80:
            insights.append({
                'type': 'positive',
                'icon': '🌟',
                'title': 'Excellent Consistency!',
                'message': f'{child.name} is showing great dedication with {engagement:.0f}% engagement.',
            })
        elif engagement < 50:
            insights.append({
                'type': 'suggestion',
                'icon': '💡',
                'title': 'Build a Routine',
                'message': 'Try setting a daily learning time to build a consistent habit.',
            })

        # Skill balance insight
        if skill_mastery:
            best_skill = max(skill_mastery, key=lambda x: x.get('percentage', 0))
            weakest_skill = min(skill_mastery, key=lambda x: x.get('percentage', 0))

            if best_skill['percentage'] > 60:
                insights.append({
                    'type': 'positive',
                    'icon': best_skill.get('icon', '⭐'),
                    'title': f'Strong in {best_skill["skill"]}',
                    'message': f'{child.name} excels at {best_skill["skill"]} with {best_skill["percentage"]:.0f}% mastery!',
                })

            if weakest_skill['percentage'] < 30 and len(skill_mastery) > 1:
                insights.append({
                    'type': 'suggestion',
                    'icon': '📈',
                    'title': f'Focus on {weakest_skill["skill"]}',
                    'message': f'Spending more time on {weakest_skill["skill"]} could help balance learning.',
                })

        # Time insight
        avg_time = overall_stats.get('avg_time_per_day', 0)
        if avg_time >= 20:
            insights.append({
                'type': 'positive',
                'icon': '⏱️',
                'title': 'Great Time Investment',
                'message': f'Averaging {avg_time:.0f} minutes per day - excellent dedication!',
            })
        elif avg_time < 10 and avg_time > 0:
            insights.append({
                'type': 'suggestion',
                'icon': '⏰',
                'title': 'Try Longer Sessions',
                'message': 'Aim for 15-20 minute sessions for better retention.',
            })

        return insights[:5]  # Limit to 5 insights

    @classmethod
    def get_monthly_comparison(cls, child_id: str, months: int = 3) -> Dict[str, Any]:
        """Get month-over-month comparison data."""
        from apps.children.models import Child
        from apps.progress.models import DailyProgress

        try:
            child = Child.objects.get(id=child_id)
        except Child.DoesNotExist:
            return {'error': 'Child not found'}

        monthly_data = []
        today = timezone.now().date()

        for i in range(months):
            # Calculate month boundaries
            if i == 0:
                end = today
            else:
                end = (today.replace(day=1) - timedelta(days=1))
                for _ in range(i - 1):
                    end = (end.replace(day=1) - timedelta(days=1))

            start = end.replace(day=1)

            # Get stats for this month
            progress = DailyProgress.objects.filter(
                child=child,
                date__gte=start,
                date__lte=end
            ).aggregate(
                time=Sum('time_spent_minutes'),
                points=Sum('points_earned'),
                days=Count('id', filter=F('time_spent_minutes') > 0),
            )

            monthly_data.append({
                'month': start.strftime('%B %Y'),
                'start_date': start.isoformat(),
                'end_date': end.isoformat(),
                'total_time_minutes': progress['time'] or 0,
                'points_earned': progress['points'] or 0,
                'days_active': progress['days'] or 0,
            })

        return {
            'child_id': child_id,
            'months': monthly_data,
        }

    @staticmethod
    def _calculate_age(date_of_birth) -> Optional[int]:
        """Calculate age from date of birth."""
        if not date_of_birth:
            return None
        today = date.today()
        age = today.year - date_of_birth.year
        if (today.month, today.day) < (date_of_birth.month, date_of_birth.day):
            age -= 1
        return age

    @staticmethod
    def _get_mastery_level(ratio: float) -> str:
        """Convert mastery ratio to level string."""
        if ratio >= 0.9:
            return 'Expert'
        elif ratio >= 0.7:
            return 'Advanced'
        elif ratio >= 0.5:
            return 'Intermediate'
        elif ratio >= 0.25:
            return 'Beginner'
        else:
            return 'Getting Started'

    @staticmethod
    def _get_streak_status(streak: int) -> str:
        """Get motivational streak status message."""
        if streak >= 30:
            return 'On Fire! 🔥'
        elif streak >= 14:
            return 'Two Week Champion! 🏆'
        elif streak >= 7:
            return 'Week Warrior! ⭐'
        elif streak >= 3:
            return 'Building Momentum! 💪'
        elif streak >= 1:
            return 'Keep Going! 🌱'
        else:
            return 'Start Today! 🚀'
