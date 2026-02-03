"""Peppi narration URL configuration."""
from django.urls import path
from .peppi_views import (
    PeppiNarrateStoryView,
    PeppiNarrateTextView,
    PeppiNarratePageView,
    PeppiNarrateSongView,
)

app_name = 'peppi'

urlpatterns = [
    # Full story narration
    path(
        'narrate/story/<uuid:story_id>/',
        PeppiNarrateStoryView.as_view(),
        name='narrate-story'
    ),

    # Single page narration
    path(
        'narrate/story/<uuid:story_id>/page/<int:page_number>/',
        PeppiNarratePageView.as_view(),
        name='narrate-page'
    ),

    # Song narration (limited to 1 song cache during testing)
    path(
        'narrate/song/<uuid:song_id>/',
        PeppiNarrateSongView.as_view(),
        name='narrate-song'
    ),

    # Arbitrary text narration
    path('narrate/', PeppiNarrateTextView.as_view(), name='narrate-text'),
]
