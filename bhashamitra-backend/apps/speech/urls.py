"""Speech app URL configuration."""
from django.urls import path, include
from . import views

app_name = 'speech'

urlpatterns = [
    # Main TTS endpoint (Hugging Face Indic Parler-TTS)
    path('tts/', views.TextToSpeechView.as_view(), name='tts'),

    # Speech-to-Text endpoint (Google Cloud STT with pronunciation evaluation)
    path('stt/', views.SpeechToTextView.as_view(), name='stt'),

    # Story-specific audio
    path(
        'stories/<uuid:story_id>/pages/<int:page_number>/audio/',
        views.StoryPageAudioView.as_view(),
        name='story-page-audio'
    ),

    # Curriculum audio (pre-generated, available for free tier)
    path('curriculum/', views.CurriculumAudioListView.as_view(), name='curriculum-list'),
    path(
        'curriculum/<str:content_type>/<str:content_id>/',
        views.CurriculumAudioView.as_view(),
        name='curriculum-audio'
    ),

    # Service status
    path('status/', views.TTSStatusView.as_view(), name='status'),

    # Pre-warm cache (admin only)
    path('prewarm/<uuid:story_id>/', views.PrewarmStoryAudioView.as_view(), name='prewarm'),

    # Audio upload for mimic recordings
    path('upload-audio/', views.AudioUploadView.as_view(), name='upload-audio'),

    # Mimic Challenge Endpoints
    path('mimic/', include('apps.speech.mimic_urls')),
]
