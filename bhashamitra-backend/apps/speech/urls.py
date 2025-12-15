"""Speech app URL configuration."""
from django.urls import path
from . import views

app_name = 'speech'

urlpatterns = [
    # Main TTS endpoint (Hugging Face Indic Parler-TTS)
    path('tts/', views.TextToSpeechView.as_view(), name='tts'),

    # Story-specific audio
    path(
        'stories/<uuid:story_id>/pages/<int:page_number>/audio/',
        views.StoryPageAudioView.as_view(),
        name='story-page-audio'
    ),

    # Service status
    path('status/', views.TTSStatusView.as_view(), name='status'),

    # Pre-warm cache (admin only)
    path('prewarm/<uuid:story_id>/', views.PrewarmStoryAudioView.as_view(), name='prewarm'),
]
