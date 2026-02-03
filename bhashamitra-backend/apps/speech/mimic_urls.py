"""Peppi Mimic URL configuration (child-specific routes)."""
from django.urls import path
from apps.speech.views import (
    MimicChallengeListView,
    MimicChallengeDetailView,
    MimicAttemptSubmitView,
    MimicProgressView,
    MimicAttemptShareView,
)

app_name = 'mimic'

urlpatterns = [
    # Challenge list
    path(
        'challenges/',
        MimicChallengeListView.as_view(),
        name='challenge-list'
    ),

    # Challenge detail
    path(
        'challenges/<uuid:challenge_id>/',
        MimicChallengeDetailView.as_view(),
        name='challenge-detail'
    ),

    # Submit attempt
    path(
        'challenges/<uuid:challenge_id>/attempt/',
        MimicAttemptSubmitView.as_view(),
        name='submit-attempt'
    ),

    # Progress summary
    path(
        'progress/',
        MimicProgressView.as_view(),
        name='progress'
    ),

    # Mark attempt as shared
    path(
        'attempts/<uuid:attempt_id>/share/',
        MimicAttemptShareView.as_view(),
        name='share-attempt'
    ),
]
