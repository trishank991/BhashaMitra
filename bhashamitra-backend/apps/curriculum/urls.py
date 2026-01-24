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
    # Curriculum Hierarchy
    CurriculumLevelListView,
    CurriculumLevelDetailView,
    CurriculumModuleListView,
    CurriculumModuleDetailView,
    LessonListView,
    LessonDetailView,
    LessonProgressUpdateView,
    ChildLevelProgressView,
    ChildHomepageProgressView,
    # Songs
    song_list,
    song_detail,
    songs_by_level,
    # Peppi
    peppi_greeting,
    peppi_teach_word,
    peppi_feedback,
    peppi_context,
    # Teacher & Classroom
    TeacherListView,
    TeacherDetailView,
    TeacherByCharacterView,
    ClassroomListView,
    ClassroomDetailView,
    ClassroomByLevelView,
)

app_name = 'curriculum'

urlpatterns = [
    # ========== CURRICULUM HIERARCHY ==========
    path('levels/', CurriculumLevelListView.as_view(), name='level-list'),
    path('levels/<uuid:pk>/', CurriculumLevelDetailView.as_view(), name='level-detail'),
    path('levels/<uuid:level_id>/modules/', CurriculumModuleListView.as_view(), name='level-modules'),
    path('modules/<uuid:pk>/', CurriculumModuleDetailView.as_view(), name='module-detail'),
    path('modules/<uuid:module_id>/lessons/', LessonListView.as_view(), name='module-lessons'),
    path('lessons/<uuid:pk>/', LessonDetailView.as_view(), name='lesson-detail'),
    path('lessons/<uuid:lesson_id>/progress/', LessonProgressUpdateView.as_view(), name='lesson-progress'),
    path('progress/levels/', ChildLevelProgressView.as_view(), name='child-level-progress'),
    path('children/<uuid:child_id>/homepage-progress/', ChildHomepageProgressView.as_view(), name='child-homepage-progress'),

    # ========== ALPHABET (with child_id) ==========
    path('children/<uuid:child_id>/alphabet/scripts/', ScriptListView.as_view(), name='child-script-list'),
    path('children/<uuid:child_id>/alphabet/scripts/<uuid:pk>/', ScriptDetailView.as_view(), name='child-script-detail'),
    path('children/<uuid:child_id>/alphabet/scripts/<uuid:pk>/letters/', ScriptLettersView.as_view(), name='child-script-letters'),
    path('children/<uuid:child_id>/alphabet/letters/', LetterListView.as_view(), name='child-letter-list'),
    path('children/<uuid:child_id>/alphabet/letters/<uuid:pk>/', LetterDetailView.as_view(), name='child-letter-detail'),
    path('children/<uuid:child_id>/alphabet/letters/<uuid:pk>/progress/', LetterProgressView.as_view(), name='child-letter-progress'),
    path('children/<uuid:child_id>/alphabet/progress/', AlphabetProgressView.as_view(), name='child-alphabet-progress'),
    # Legacy routes without child_id (for backward compatibility)
    path('alphabet/scripts/', ScriptListView.as_view(), name='script-list'),
    path('alphabet/scripts/<uuid:pk>/', ScriptDetailView.as_view(), name='script-detail'),
    path('alphabet/scripts/<uuid:pk>/letters/', ScriptLettersView.as_view(), name='script-letters'),
    path('alphabet/letters/', LetterListView.as_view(), name='letter-list'),
    path('alphabet/letters/<uuid:pk>/', LetterDetailView.as_view(), name='letter-detail'),
    path('alphabet/letters/<uuid:pk>/progress/', LetterProgressView.as_view(), name='letter-progress'),
    path('alphabet/progress/', AlphabetProgressView.as_view(), name='alphabet-progress'),

    # ========== VOCABULARY (with child_id) ==========
    path('children/<uuid:child_id>/vocabulary/themes/', VocabularyThemeListView.as_view(), name='child-theme-list'),
    path('children/<uuid:child_id>/vocabulary/themes/<uuid:pk>/', ThemeDetailView.as_view(), name='child-theme-detail'),
    path('children/<uuid:child_id>/vocabulary/themes/<uuid:pk>/words/', ThemeWordsView.as_view(), name='child-theme-words'),
    path('children/<uuid:child_id>/vocabulary/themes/<uuid:pk>/stats/', ThemeStatsView.as_view(), name='child-theme-stats'),
    path('children/<uuid:child_id>/vocabulary/words/<uuid:pk>/', WordDetailView.as_view(), name='child-word-detail'),
    path('children/<uuid:child_id>/vocabulary/flashcards/due/', FlashcardsDueView.as_view(), name='child-flashcards-due'),
    path('children/<uuid:child_id>/vocabulary/flashcards/review/', FlashcardReviewView.as_view(), name='child-flashcard-review'),
    path('children/<uuid:child_id>/vocabulary/flashcards/session/', FlashcardSessionView.as_view(), name='child-flashcard-session'),
    # Legacy routes without child_id
    path('vocabulary/themes/', VocabularyThemeListView.as_view(), name='theme-list'),
    path('vocabulary/themes/<uuid:pk>/', ThemeDetailView.as_view(), name='theme-detail'),
    path('vocabulary/themes/<uuid:pk>/words/', ThemeWordsView.as_view(), name='theme-words'),
    path('vocabulary/themes/<uuid:pk>/stats/', ThemeStatsView.as_view(), name='theme-stats'),
    path('vocabulary/words/<uuid:pk>/', WordDetailView.as_view(), name='word-detail'),
    path('vocabulary/flashcards/due/', FlashcardsDueView.as_view(), name='flashcards-due'),
    path('vocabulary/flashcards/review/', FlashcardReviewView.as_view(), name='flashcard-review'),
    path('vocabulary/flashcards/session/', FlashcardSessionView.as_view(), name='flashcard-session'),

    # ========== CHILDREN NESTED ROUTES ==========
    path('children/<uuid:child_id>/curriculum/grammar/topics/', GrammarTopicListView.as_view(), name='child-grammar-topics'),

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

    # ========== SONGS ==========
    path('songs/', song_list, name='song-list'),
    path('songs/<uuid:song_id>/', song_detail, name='song-detail'),
    path('songs/level/<str:level_code>/', songs_by_level, name='songs-by-level'),

    # ========== PEPPI AI ==========
    path('peppi/<uuid:child_id>/greeting/', peppi_greeting, name='peppi-greeting'),
    path('peppi/<uuid:child_id>/teach-word/', peppi_teach_word, name='peppi-teach-word'),
    path('peppi/<uuid:child_id>/feedback/', peppi_feedback, name='peppi-feedback'),
    path('peppi/<uuid:child_id>/context/', peppi_context, name='peppi-context'),

    # ========== TEACHERS ==========
    path('teachers/', TeacherListView.as_view(), name='teacher-list'),
    path('teachers/<uuid:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
    path('teachers/character/<str:character_type>/', TeacherByCharacterView.as_view(), name='teacher-by-character'),

    # ========== CLASSROOMS ==========
    path('classrooms/', ClassroomListView.as_view(), name='classroom-list'),
    path('classrooms/<uuid:pk>/', ClassroomDetailView.as_view(), name='classroom-detail'),
    path('classrooms/level/<str:level_code>/', ClassroomByLevelView.as_view(), name='classroom-by-level'),
]