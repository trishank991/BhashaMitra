"""
Parent Engagement API URL Configuration.
"""

from django.urls import path
from .views import (
    ParentDashboardView,
    ParentChildrenListView,
    ChildSummaryView,
    ChildDetailedProgressView,
    ChildActivityView,
    ChildStatsView,
    ChildWeeklyReportView,
    ChildGoalsView,
    GoalDetailView,
    ProgressUpdateView,
    ParentPreferencesView,
    ParentActivitiesView,
    ChildReportCardView,
    ChildSkillsBreakdownView,
    ChildMonthlyStatsView,
)

app_name = 'parent_engagement'

urlpatterns = [
    # Parent Dashboard - Summary of all children
    path('dashboard/', ParentDashboardView.as_view(), name='dashboard'),

    # Parent preferences
    path('preferences/', ParentPreferencesView.as_view(), name='preferences'),

    # Suggested parent-child activities
    path('activities/', ParentActivitiesView.as_view(), name='activities'),

    # List all children for the parent
    path('children/', ParentChildrenListView.as_view(), name='children-list'),

    # Child-specific endpoints
    path(
        'children/<uuid:child_id>/summary/',
        ChildSummaryView.as_view(),
        name='child-summary'
    ),
    path(
        'children/<uuid:child_id>/activity/',
        ChildActivityView.as_view(),
        name='child-activity'
    ),
    path(
        'children/<uuid:child_id>/progress/',
        ChildDetailedProgressView.as_view(),
        name='child-detailed-progress'
    ),
    path(
        'children/<uuid:child_id>/stats/',
        ChildStatsView.as_view(),
        name='child-stats'
    ),
    path(
        'children/<uuid:child_id>/weekly-report/',
        ChildWeeklyReportView.as_view(),
        name='child-weekly-report'
    ),
    path(
        'children/<uuid:child_id>/goals/',
        ChildGoalsView.as_view(),
        name='child-goals'
    ),
    path(
        'children/<uuid:child_id>/goals/<int:goal_id>/',
        GoalDetailView.as_view(),
        name='goal-detail'
    ),
    path(
        'children/<uuid:child_id>/progress-update/',
        ProgressUpdateView.as_view(),
        name='child-progress-update'
    ),
    # Report Card endpoints
    path(
        'children/<uuid:child_id>/report-card/',
        ChildReportCardView.as_view(),
        name='child-report-card'
    ),
    path(
        'children/<uuid:child_id>/skills/',
        ChildSkillsBreakdownView.as_view(),
        name='child-skills'
    ),
    path(
        'children/<uuid:child_id>/monthly-stats/',
        ChildMonthlyStatsView.as_view(),
        name='child-monthly-stats'
    ),
]
