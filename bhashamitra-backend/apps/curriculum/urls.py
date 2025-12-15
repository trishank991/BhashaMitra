"""Curriculum URL configuration."""
from django.urls import path
from .views import (
    # Alphabet
    ScriptListView,
    ScriptDetailView,
    ScriptLettersView,
    LetterListView,
    LetterDetailView,
    LetterProgressView,
    AlphabetProgressView,
    # Vocabulary
    VocabularyThemeListView,
    ThemeDetailView,
    ThemeWordsView,
    ThemeStatsView,
    WordDetailView,
    FlashcardsDueView,
    FlashcardReviewView,
    FlashcardSessionView,
    # Grammar
    GrammarTopicListView,
    GrammarTopicDetailView,
    TopicRulesView,
    TopicExercisesView,
    ExerciseDetailView,
    ExerciseSubmitView,
    GrammarProgressView,
    # Games
    GameListView,
    GameDetailView,
    GameStartView,
    GameSubmitView,
    GameLeaderboardView,
    GlobalLeaderboardView,
    GameHistoryView,
    # Assessment
    AssessmentListView,
    AssessmentDetailView,
    AssessmentStartView,
    AssessmentSubmitView,
    AssessmentAttemptsView,
    AttemptDetailView,
    CertificateListView,
    CertificateDetailView,
)

app_name = 'curriculum'

urlpatterns = [
    # ========== ALPHABET ==========
    path('alphabet/scripts/', ScriptListView.as_view(), name='script-list'),
    path('alphabet/scripts/<uuid:pk>/', ScriptDetailView.as_view(), name='script-detail'),
    path('alphabet/scripts/<uuid:pk>/letters/', ScriptLettersView.as_view(), name='script-letters'),
    path('alphabet/letters/', LetterListView.as_view(), name='letter-list'),
    path('alphabet/letters/<uuid:pk>/', LetterDetailView.as_view(), name='letter-detail'),
    path('alphabet/letters/<uuid:pk>/progress/', LetterProgressView.as_view(), name='letter-progress'),
    path('alphabet/progress/', AlphabetProgressView.as_view(), name='alphabet-progress'),

    # ========== VOCABULARY ==========
    path('vocabulary/themes/', VocabularyThemeListView.as_view(), name='theme-list'),
    path('vocabulary/themes/<uuid:pk>/', ThemeDetailView.as_view(), name='theme-detail'),
    path('vocabulary/themes/<uuid:pk>/words/', ThemeWordsView.as_view(), name='theme-words'),
    path('vocabulary/themes/<uuid:pk>/stats/', ThemeStatsView.as_view(), name='theme-stats'),
    path('vocabulary/words/<uuid:pk>/', WordDetailView.as_view(), name='word-detail'),
    path('vocabulary/flashcards/due/', FlashcardsDueView.as_view(), name='flashcards-due'),
    path('vocabulary/flashcards/review/', FlashcardReviewView.as_view(), name='flashcard-review'),
    path('vocabulary/flashcards/session/', FlashcardSessionView.as_view(), name='flashcard-session'),

    # ========== GRAMMAR ==========
    path('grammar/topics/', GrammarTopicListView.as_view(), name='topic-list'),
    path('grammar/topics/<uuid:pk>/', GrammarTopicDetailView.as_view(), name='topic-detail'),
    path('grammar/topics/<uuid:pk>/rules/', TopicRulesView.as_view(), name='topic-rules'),
    path('grammar/topics/<uuid:pk>/exercises/', TopicExercisesView.as_view(), name='topic-exercises'),
    path('grammar/exercises/<uuid:pk>/', ExerciseDetailView.as_view(), name='exercise-detail'),
    path('grammar/exercises/<uuid:pk>/submit/', ExerciseSubmitView.as_view(), name='exercise-submit'),
    path('grammar/progress/', GrammarProgressView.as_view(), name='grammar-progress'),

    # ========== GAMES ==========
    path('games/', GameListView.as_view(), name='game-list'),
    path('games/history/', GameHistoryView.as_view(), name='game-history'),
    path('games/leaderboard/', GlobalLeaderboardView.as_view(), name='global-leaderboard'),
    path('games/<uuid:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('games/<uuid:pk>/start/', GameStartView.as_view(), name='game-start'),
    path('games/<uuid:pk>/submit/', GameSubmitView.as_view(), name='game-submit'),
    path('games/<uuid:pk>/leaderboard/', GameLeaderboardView.as_view(), name='game-leaderboard'),

    # ========== ASSESSMENTS ==========
    path('assessments/', AssessmentListView.as_view(), name='assessment-list'),
    path('assessments/attempts/', AssessmentAttemptsView.as_view(), name='assessment-attempts'),
    path('assessments/certificates/', CertificateListView.as_view(), name='certificate-list'),
    path('assessments/certificates/<str:certificate_id>/', CertificateDetailView.as_view(), name='certificate-detail'),
    path('assessments/<uuid:pk>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/<uuid:pk>/start/', AssessmentStartView.as_view(), name='assessment-start'),
    path('assessments/<uuid:pk>/submit/', AssessmentSubmitView.as_view(), name='assessment-submit'),
    path('assessments/attempts/<uuid:pk>/', AttemptDetailView.as_view(), name='attempt-detail'),
]
