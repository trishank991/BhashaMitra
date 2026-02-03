"""
Parent Dashboard API Views.

Provides endpoints for parents to monitor their children's learning progress.
"""

from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Sum, Count, Avg
from datetime import timedelta

from apps.children.models import Child
from apps.progress.models import DailyProgress, ActivityLog
from apps.parent_engagement.models import LearningGoal

from .serializers import (
    ChildBasicSerializer,
    ChildSummarySerializer,
    ChildProgressSerializer,
    ChildStatsSerializer,
    ActivityLogSerializer,
    DailyProgressSerializer,
    LearningGoalSerializer,
    WeeklyReportSerializer,
    ProgressUpdateSerializer,
    GoalCreateSerializer,
)


class ParentDashboardView(APIView):
    """
    GET /api/v1/parent/dashboard/

    Returns summary for all children of the logged-in parent.
    Data per child: name, avatar, level, streak, XP this week, recent activity count.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        children = Child.objects.filter(
            user=request.user,
            deleted_at__isnull=True
        ).order_by('-created_at')

        serializer = ChildSummarySerializer(children, many=True)

        return Response({
            'children': serializer.data,
            'total_children': children.count(),
        })


class ParentChildrenListView(generics.ListAPIView):
    """
    GET /api/parent/children/

    List all children associated with the authenticated parent.
    Returns basic info and summary stats for each child.
    """
    serializer_class = ChildBasicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Child.objects.filter(
            user=self.request.user,
            deleted_at__isnull=True
        ).order_by('-created_at')


class ChildSummaryView(APIView):
    """
    GET /api/parent/children/{child_id}/summary/

    Get detailed summary of a child's learning progress.
    Includes weekly stats, current streak, and achievements.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        today = timezone.now().date()
        week_start = today - timedelta(days=today.weekday())

        # Get this week's progress
        weekly_progress = DailyProgress.objects.filter(
            child=child,
            date__gte=week_start,
            date__lte=today
        ).aggregate(
            total_time=Sum('time_spent_minutes'),
            total_lessons=Sum('lessons_completed'),
            total_exercises=Sum('exercises_completed'),
            total_games=Sum('games_played'),
            total_points=Sum('points_earned'),
        )

        # Calculate current streak
        streak = self._calculate_streak(child, today)

        # Get recent achievements
        recent_achievements = ActivityLog.objects.filter(
            child=child,
            activity_type__in=['BADGE_EARNED', 'LEVEL_UP', 'STREAK_MILESTONE'],
            created_at__gte=today - timedelta(days=30)
        ).count()

        # Get active goals progress
        active_goals = LearningGoal.objects.filter(
            child=child,
            is_active=True,
            end_date__gte=today
        )

        goals_data = LearningGoalSerializer(active_goals, many=True).data

        return Response({
            'child': ChildBasicSerializer(child).data,
            'weekly_summary': {
                'time_spent_minutes': weekly_progress['total_time'] or 0,
                'lessons_completed': weekly_progress['total_lessons'] or 0,
                'exercises_completed': weekly_progress['total_exercises'] or 0,
                'games_played': weekly_progress['total_games'] or 0,
                'points_earned': weekly_progress['total_points'] or 0,
            },
            'current_streak': streak,
            'recent_achievements': recent_achievements,
            'active_goals': goals_data,
        })

    def _calculate_streak(self, child, today):
        """Calculate consecutive days of activity."""
        streak = 0
        current_date = today

        while True:
            has_activity = DailyProgress.objects.filter(
                child=child,
                date=current_date,
                time_spent_minutes__gt=0
            ).exists()

            if has_activity:
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break

            # Cap at 365 to prevent infinite loops
            if streak >= 365:
                break

        return streak


class ChildActivityView(generics.ListAPIView):
    """
    GET /api/parent/children/{child_id}/activity/

    Get recent activity log for a child.
    Supports pagination and filtering by activity type.
    """
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        child_id = self.kwargs['child_id']
        child = get_object_or_404(
            Child,
            id=child_id,
            user=self.request.user,
            deleted_at__isnull=True
        )

        queryset = ActivityLog.objects.filter(child=child)

        # Filter by activity type if provided
        activity_type = self.request.query_params.get('type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type.upper())

        # Filter by date range
        days = self.request.query_params.get('days', 7)
        try:
            days = int(days)
        except ValueError:
            days = 7

        since_date = timezone.now() - timedelta(days=days)
        queryset = queryset.filter(created_at__gte=since_date)

        return queryset.order_by('-created_at')


class ChildWeeklyReportView(APIView):
    """
    GET /api/parent/children/{child_id}/weekly-report/

    Get comprehensive weekly progress report for a child.
    Includes daily breakdown, comparisons, and suggestions.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        today = timezone.now().date()
        week_start = today - timedelta(days=6)  # Last 7 days

        # Get daily progress for the week
        daily_progress = DailyProgress.objects.filter(
            child=child,
            date__gte=week_start,
            date__lte=today
        ).order_by('date')

        daily_data = DailyProgressSerializer(daily_progress, many=True).data

        # Calculate weekly totals
        totals = daily_progress.aggregate(
            total_time=Sum('time_spent_minutes'),
            total_lessons=Sum('lessons_completed'),
            total_exercises=Sum('exercises_completed'),
            total_games=Sum('games_played'),
            total_points=Sum('points_earned'),
        )

        # Get previous week for comparison
        prev_week_start = week_start - timedelta(days=7)
        prev_week_end = week_start - timedelta(days=1)

        prev_totals = DailyProgress.objects.filter(
            child=child,
            date__gte=prev_week_start,
            date__lte=prev_week_end
        ).aggregate(
            total_time=Sum('time_spent_minutes'),
            total_points=Sum('points_earned'),
        )

        # Calculate comparison percentages
        current_time = totals['total_time'] or 0
        prev_time = prev_totals['total_time'] or 1  # Avoid division by zero
        time_change = ((current_time - prev_time) / prev_time) * 100 if prev_time else 0

        current_points = totals['total_points'] or 0
        prev_points = prev_totals['total_points'] or 1
        points_change = ((current_points - prev_points) / prev_points) * 100 if prev_points else 0

        # Generate highlights
        highlights = self._generate_highlights(child, daily_progress, totals)

        # Generate suggestions
        suggestions = self._generate_suggestions(child, totals)

        report_data = {
            'daily_data': daily_data,
            'summary': {
                'total_time_minutes': current_time,
                'total_lessons': totals['total_lessons'] or 0,
                'total_exercises': totals['total_exercises'] or 0,
                'total_games': totals['total_games'] or 0,
                'total_points': current_points,
                'days_active': daily_progress.filter(time_spent_minutes__gt=0).count(),
            },
            'comparison': {
                'time_change_percent': round(time_change, 1),
                'points_change_percent': round(points_change, 1),
                'trend': 'up' if time_change > 0 else ('down' if time_change < 0 else 'stable'),
            },
            'highlights': highlights,
            'suggestions': suggestions,
        }

        return Response(WeeklyReportSerializer(report_data).data)

    def _generate_highlights(self, child, daily_progress, totals):
        """Generate positive highlights from the week."""
        highlights = []

        # Check for streaks
        active_days = daily_progress.filter(time_spent_minutes__gt=0).count()
        if active_days == 7:
            highlights.append({
                'type': 'streak',
                'message': 'Perfect week! Active all 7 days!',
                'icon': '🔥',
            })
        elif active_days >= 5:
            highlights.append({
                'type': 'streak',
                'message': f'Great consistency! Active {active_days} days this week',
                'icon': '⭐',
            })

        # Check for milestones
        total_lessons = totals['total_lessons'] or 0
        if total_lessons >= 10:
            highlights.append({
                'type': 'lessons',
                'message': f'Completed {total_lessons} lessons this week!',
                'icon': '📚',
            })

        # Check for new badges
        new_badges = ActivityLog.objects.filter(
            child=child,
            activity_type='BADGE_EARNED',
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()

        if new_badges > 0:
            highlights.append({
                'type': 'badge',
                'message': f'Earned {new_badges} new badge{"s" if new_badges > 1 else ""}!',
                'icon': '🏆',
            })

        return highlights[:5]  # Limit to 5 highlights

    def _generate_suggestions(self, child, totals):
        """Generate helpful suggestions for parents."""
        suggestions = []

        total_time = totals['total_time'] or 0
        total_games = totals['total_games'] or 0

        # Suggest more learning time
        if total_time < 60:  # Less than 1 hour total
            suggestions.append({
                'type': 'time',
                'message': 'Try to aim for at least 15 minutes of learning each day',
                'action': 'Set a daily reminder',
            })

        # Suggest games for engagement
        if total_games == 0:
            suggestions.append({
                'type': 'games',
                'message': 'Games make learning fun! Try the letter matching game together',
                'action': 'Play a game',
            })

        # Suggest parent involvement
        suggestions.append({
            'type': 'bonding',
            'message': 'Practice speaking Hindi together during meals or car rides',
            'action': 'Family activity',
        })

        return suggestions[:3]  # Limit to 3 suggestions


class ChildGoalsView(APIView):
    """
    GET /api/parent/children/{child_id}/goals/
    POST /api/parent/children/{child_id}/goals/

    List and create learning goals for a child.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        goals = LearningGoal.objects.filter(
            child=child,
            is_active=True
        ).order_by('-created_at')

        return Response({
            'goals': LearningGoalSerializer(goals, many=True).data,
            'count': goals.count(),
        })

    def post(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        serializer = GoalCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        goal_type = data['type']
        target = data['target']
        deadline = data.get('deadline')

        # Map API goal types to model goal types
        goal_type_map = {
            'daily_time': 'DAILY_MINUTES',
            'weekly_lessons': 'WEEKLY_STORIES',
            'weekly_words': 'MONTHLY_POINTS',  # Reuse for words
            'streak': 'LEVEL_TARGET',  # Reuse for streak
        }

        goal = LearningGoal.objects.create(
            child=child,
            goal_type=goal_type_map.get(goal_type, 'DAILY_MINUTES'),
            target_value=target,
            current_value=0,
            start_date=timezone.now().date(),
            end_date=deadline or (timezone.now().date() + timedelta(days=7)),
            is_active=True,
        )

        return Response(
            LearningGoalSerializer(goal).data,
            status=status.HTTP_201_CREATED
        )


class ProgressUpdateView(APIView):
    """
    POST /api/parent/children/{child_id}/progress/

    Record progress update for a child's learning session.
    Called by the frontend after completing lessons, exercises, or games.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        serializer = ProgressUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        activity_type = data['type']
        duration = data.get('duration_minutes', 0)
        points = data.get('points_earned', 0)
        details = data.get('details', {})

        today = timezone.now().date()

        # Get or create today's progress
        daily_progress, created = DailyProgress.objects.get_or_create(
            child=child,
            date=today,
            defaults={
                'time_spent_minutes': 0,
                'lessons_completed': 0,
                'exercises_completed': 0,
                'games_played': 0,
                'points_earned': 0,
            }
        )

        # Update progress based on activity type
        daily_progress.time_spent_minutes += duration
        daily_progress.points_earned += points

        if activity_type == 'lesson':
            daily_progress.lessons_completed += 1
            activity_log_type = 'LESSON_COMPLETED'
        elif activity_type == 'exercise':
            daily_progress.exercises_completed += 1
            activity_log_type = 'EXERCISE_COMPLETED'
        elif activity_type == 'game':
            daily_progress.games_played += 1
            activity_log_type = 'GAME_COMPLETED'
        else:
            activity_log_type = 'LESSON_COMPLETED'

        daily_progress.save()

        # Update child's total points
        child.total_points += points
        child.save(update_fields=['total_points'])

        # Create activity log entry
        description = details.get('description', f'Completed {activity_type}')
        ActivityLog.objects.create(
            child=child,
            activity_type=activity_log_type,
            description=description,
            points_earned=points,
        )

        # Update relevant goals
        self._update_goals(child, activity_type, duration, today)

        return Response({
            'success': True,
            'daily_progress': DailyProgressSerializer(daily_progress).data,
            'total_points': child.total_points,
        })

    def _update_goals(self, child, activity_type, duration, today):
        """Update progress on active goals."""
        active_goals = LearningGoal.objects.filter(
            child=child,
            is_active=True,
            end_date__gte=today
        )

        for goal in active_goals:
            updated = False

            if goal.goal_type == 'DAILY_MINUTES':
                goal.current_value = min(goal.current_value + duration, goal.target_value)
                updated = True
            elif goal.goal_type == 'WEEKLY_STORIES' and activity_type == 'lesson':
                goal.current_value += 1
                updated = True
            elif goal.goal_type == 'MONTHLY_POINTS' and activity_type == 'lesson':
                # Assume each lesson teaches ~3 words
                goal.current_value += 3
                updated = True

            if updated:
                goal.save(update_fields=['current_value'])

                # Check if goal completed
                if goal.current_value >= goal.target_value:
                    # Generate title from goal type and target
                    goal_titles = {
                        'DAILY_MINUTES': f'Learn for {goal.target_value} minutes daily',
                        'WEEKLY_STORIES': f'Complete {goal.target_value} stories this week',
                        'MONTHLY_POINTS': f'Earn {goal.target_value} points this month',
                        'LEVEL_TARGET': f'Reach level {goal.target_value}',
                    }
                    goal_title = goal_titles.get(goal.goal_type, 'Learning goal')
                    ActivityLog.objects.create(
                        child=child,
                        activity_type='BADGE_EARNED',
                        description=f'Goal completed: {goal_title}',
                        points_earned=50,  # Bonus points for completing goal
                    )
                    child.total_points += 50
                    child.save(update_fields=['total_points'])


class ParentPreferencesView(APIView):
    """
    GET /api/parent/preferences/
    PUT /api/parent/preferences/

    Get and update parent notification preferences.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.parent_engagement.models import ParentPreferences

        # Get or create preferences for this user
        preferences, created = ParentPreferences.objects.get_or_create(
            user=request.user,
            defaults={
                'notification_frequency': 'WEEKLY',
                'email_reports': True,
                'push_notifications': True,
                'sms_alerts': False,
                'preferred_report_day': 0,
                'timezone': 'Pacific/Auckland',
            }
        )

        return Response({
            'id': preferences.id,
            'notification_frequency': preferences.notification_frequency,
            'email_reports': preferences.email_reports,
            'push_notifications': preferences.push_notifications,
            'sms_alerts': preferences.sms_alerts,
            'preferred_report_day': preferences.preferred_report_day,
            'timezone': preferences.timezone,
            'notification_options': dict(ParentPreferences.NotificationFrequency.choices),
        })

    def put(self, request):
        from apps.parent_engagement.models import ParentPreferences
        from .serializers import ParentPreferencesSerializer

        preferences, _ = ParentPreferences.objects.get_or_create(
            user=request.user,
            defaults={
                'notification_frequency': 'WEEKLY',
                'email_reports': True,
                'push_notifications': True,
            }
        )

        serializer = ParentPreferencesSerializer(
            preferences,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'success': True,
            'preferences': serializer.data,
        })


class GoalDetailView(APIView):
    """
    PUT /api/parent/children/{child_id}/goals/{goal_id}/
    DELETE /api/parent/children/{child_id}/goals/{goal_id}/

    Update or delete a specific learning goal.
    """
    permission_classes = [IsAuthenticated]

    def put(self, request, child_id, goal_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        goal = get_object_or_404(
            LearningGoal,
            id=goal_id,
            child=child
        )

        # Update allowed fields
        allowed_fields = ['target_value', 'end_date', 'is_active']
        for field in allowed_fields:
            if field in request.data:
                setattr(goal, field, request.data[field])

        goal.save()

        return Response({
            'success': True,
            'goal': LearningGoalSerializer(goal).data,
        })

    def delete(self, request, child_id, goal_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        goal = get_object_or_404(
            LearningGoal,
            id=goal_id,
            child=child
        )

        # Soft delete by deactivating
        goal.is_active = False
        goal.save(update_fields=['is_active'])

        return Response({
            'success': True,
            'message': 'Goal deactivated',
        })


class ParentActivitiesView(APIView):
    """
    GET /api/parent/activities/

    Get suggested parent-child activities based on child's learning.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from apps.parent_engagement.models import ParentChildActivity

        language = request.query_params.get('language', 'HINDI')
        activity_type = request.query_params.get('type')
        child_age = request.query_params.get('age')

        # Base queryset
        queryset = ParentChildActivity.objects.filter(language=language)

        # Filter by activity type
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type.upper())

        # Filter by age if provided
        if child_age:
            try:
                age = int(child_age)
                queryset = queryset.filter(min_age__lte=age, max_age__gte=age)
            except ValueError:
                pass

        # Prioritize featured activities
        queryset = queryset.order_by('-is_featured', '?')[:10]

        activities_data = []
        for activity in queryset:
            activities_data.append({
                'id': activity.id,
                'title': activity.title,
                'activity_type': activity.activity_type,
                'description': activity.description,
                'duration_minutes': activity.duration_minutes,
                'materials_needed': activity.materials_needed,
                'learning_outcomes': activity.learning_outcomes,
                'is_featured': activity.is_featured,
                'age_range': f"{activity.min_age}-{activity.max_age}",
            })

        return Response({
            'activities': activities_data,
            'activity_types': dict(ParentChildActivity.ActivityType.choices),
            'count': len(activities_data),
        })


class ChildReportCardView(APIView):
    """
    GET /api/parent/children/{child_id}/report-card/

    Get comprehensive report card for a child.

    Query Parameters:
    - period: Number of days to include (default 30, max 365)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        from apps.progress.report_card_service import ReportCardService

        # Get period from query params (default 30 days)
        period = request.query_params.get('period', 30)
        try:
            period = min(int(period), 365)
        except ValueError:
            period = 30

        report = ReportCardService.get_comprehensive_report(
            child_id=str(child.id),
            period_days=period
        )

        return Response(report)


class ChildSkillsBreakdownView(APIView):
    """
    GET /api/parent/children/{child_id}/skills/

    Get detailed skill mastery breakdown for a child.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        from apps.progress.report_card_service import ReportCardService

        skill_mastery = ReportCardService._get_skill_mastery(child)
        streak_info = ReportCardService._get_streak_info(child)

        return Response({
            'child_id': str(child.id),
            'child_name': child.name,
            'skills': skill_mastery,
            'streak': streak_info,
            'total_points': child.total_points,
            'level': child.level,
        })


class ChildMonthlyStatsView(APIView):
    """
    GET /api/parent/children/{child_id}/monthly-stats/

    Get month-over-month comparison for a child.

    Query Parameters:
    - months: Number of months to compare (default 3, max 12)
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        from apps.progress.report_card_service import ReportCardService

        months = request.query_params.get('months', 3)
        try:
            months = min(int(months), 12)
        except ValueError:
            months = 3

        comparison = ReportCardService.get_monthly_comparison(
            child_id=str(child.id),
            months=months
        )

        return Response(comparison)


class ChildDetailedProgressView(APIView):
    """
    GET /api/v1/parent/children/{child_id}/progress/

    Detailed progress for a specific child.
    Data: curriculum progress (levels completed), vocabulary stats, time spent.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        # Get curriculum progress
        from apps.curriculum.models.progress import LevelProgress, ModuleProgress, LessonProgress
        from apps.curriculum.models.vocabulary import WordProgress

        level_progress = LevelProgress.objects.filter(child=child)
        completed_levels = level_progress.filter(is_complete=True).count()
        total_modules = ModuleProgress.objects.filter(child=child).count()
        completed_modules = ModuleProgress.objects.filter(child=child, is_complete=True).count()
        completed_lessons = LessonProgress.objects.filter(child=child, is_complete=True).count()

        # Vocabulary stats
        word_progress = WordProgress.objects.filter(child=child)
        words_learned = word_progress.filter(mastered=True).count()
        words_in_progress = word_progress.filter(mastered=False).count()
        total_reviews = word_progress.aggregate(Sum('times_reviewed'))['times_reviewed__sum'] or 0

        # Time spent
        total_time = DailyProgress.objects.filter(child=child).aggregate(
            total=Sum('time_spent_minutes')
        )['total'] or 0

        # Badges
        from apps.gamification.models import ChildBadge
        badges_earned = ChildBadge.objects.filter(child=child).count()

        progress_data = {
            'curriculum_progress': {
                'current_level': child.level,
                'levels_completed': completed_levels,
                'modules_completed': completed_modules,
                'lessons_completed': completed_lessons,
                'total_modules': total_modules,
            },
            'vocabulary_stats': {
                'words_mastered': words_learned,
                'words_in_progress': words_in_progress,
                'total_reviews': total_reviews,
            },
            'time_spent': {
                'total_minutes': total_time,
                'total_hours': round(total_time / 60, 1),
            },
            'badges_earned': badges_earned,
            'current_level': child.level,
        }

        serializer = ChildProgressSerializer(progress_data)
        return Response(serializer.data)


class ChildStatsView(APIView):
    """
    GET /api/v1/parent/children/{child_id}/stats/

    Weekly/monthly stats for a child.
    Data: days active, lessons completed, words learned, games played.

    Query Parameters:
    - period: 'week' or 'month' (default: 'week')
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):
        child = get_object_or_404(
            Child,
            id=child_id,
            user=request.user,
            deleted_at__isnull=True
        )

        period = request.query_params.get('period', 'week')
        today = timezone.now().date()

        if period == 'month':
            # Last 30 days
            start_date = today - timedelta(days=30)
            period_label = 'Last 30 days'
        else:
            # This week (Monday to today)
            start_date = today - timedelta(days=today.weekday())
            period_label = 'This week'

        # Get daily progress for the period
        daily_stats = DailyProgress.objects.filter(
            child=child,
            date__gte=start_date,
            date__lte=today
        )

        # Aggregate stats
        stats = daily_stats.aggregate(
            total_lessons=Sum('lessons_completed'),
            total_games=Sum('games_played'),
            total_time=Sum('time_spent_minutes'),
            total_points=Sum('points_earned'),
        )

        # Days active
        days_active = daily_stats.filter(time_spent_minutes__gt=0).count()

        # Words learned (mastered in this period)
        from apps.curriculum.models.vocabulary import WordProgress
        start_datetime = timezone.make_aware(
            timezone.datetime.combine(start_date, timezone.datetime.min.time())
        )
        words_learned = WordProgress.objects.filter(
            child=child,
            mastered=True,
            mastered_at__gte=start_datetime
        ).count()

        stats_data = {
            'period': period_label,
            'days_active': days_active,
            'lessons_completed': stats['total_lessons'] or 0,
            'words_learned': words_learned,
            'games_played': stats['total_games'] or 0,
            'total_time_minutes': stats['total_time'] or 0,
            'total_points': stats['total_points'] or 0,
        }

        serializer = ChildStatsSerializer(stats_data)
        return Response(serializer.data)
