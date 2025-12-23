"""Curriculum views."""
from .alphabet import (
    ScriptListView,
    ScriptDetailView,
    ScriptLettersView,
    LetterListView,
    LetterDetailView,
    LetterProgressView,
    AlphabetProgressView,
)
from .vocabulary import (
    VocabularyThemeListView,
    ThemeDetailView,
    ThemeWordsView,
    ThemeStatsView,
    WordDetailView,
    FlashcardsDueView,
    FlashcardReviewView,
    FlashcardSessionView,
)
from .grammar import (
    GrammarTopicListView,
    GrammarTopicDetailView,
    TopicRulesView,
    TopicExercisesView,
    ExerciseDetailView,
    ExerciseSubmitView,
    GrammarProgressView,
)
from .games import (
    GameListView,
    GameDetailView,
    GameStartView,
    GameSubmitView,
    GameLeaderboardView,
    GlobalLeaderboardView,
    GameHistoryView,
)
from .assessment import (
    AssessmentListView,
    AssessmentDetailView,
    AssessmentStartView,
    AssessmentSubmitView,
    AssessmentAttemptsView,
    AttemptDetailView,
    CertificateListView,
    CertificateDetailView,
)
from .level import (
    CurriculumLevelListView,
    CurriculumLevelDetailView,
    CurriculumModuleListView,
    CurriculumModuleDetailView,
    LessonListView,
    LessonDetailView,
    LessonProgressUpdateView,
    ChildLevelProgressView,
    ChildHomepageProgressView,
)
from .songs import (
    song_list,
    song_detail,
    songs_by_level,
)
from .peppi import (
    peppi_greeting,
    peppi_teach_word,
    peppi_feedback,
    peppi_context,
)
from .teacher import TeacherListView, TeacherDetailView, TeacherByCharacterView
from .classroom import ClassroomListView, ClassroomDetailView, ClassroomByLevelView

__all__ = [
    # Alphabet
    'ScriptListView',
    'ScriptDetailView',
    'ScriptLettersView',
    'LetterListView',
    'LetterDetailView',
    'LetterProgressView',
    'AlphabetProgressView',
    # Vocabulary
    'VocabularyThemeListView',
    'ThemeDetailView',
    'ThemeWordsView',
    'ThemeStatsView',
    'WordDetailView',
    'FlashcardsDueView',
    'FlashcardReviewView',
    'FlashcardSessionView',
    # Grammar
    'GrammarTopicListView',
    'GrammarTopicDetailView',
    'TopicRulesView',
    'TopicExercisesView',
    'ExerciseDetailView',
    'ExerciseSubmitView',
    'GrammarProgressView',
    # Games
    'GameListView',
    'GameDetailView',
    'GameStartView',
    'GameSubmitView',
    'GameLeaderboardView',
    'GlobalLeaderboardView',
    'GameHistoryView',
    # Assessment
    'AssessmentListView',
    'AssessmentDetailView',
    'AssessmentStartView',
    'AssessmentSubmitView',
    'AssessmentAttemptsView',
    'AttemptDetailView',
    'CertificateListView',
    'CertificateDetailView',
    # Curriculum Hierarchy
    'CurriculumLevelListView',
    'CurriculumLevelDetailView',
    'CurriculumModuleListView',
    'CurriculumModuleDetailView',
    'LessonListView',
    'LessonDetailView',
    'LessonProgressUpdateView',
    'ChildLevelProgressView',
    'ChildHomepageProgressView',
    # Songs
    'song_list',
    'song_detail',
    'songs_by_level',
    # Peppi
    'peppi_greeting',
    'peppi_teach_word',
    'peppi_feedback',
    'peppi_context',
    # Teacher & Classroom
    'TeacherListView',
    'TeacherDetailView',
    'TeacherByCharacterView',
    'ClassroomListView',
    'ClassroomDetailView',
    'ClassroomByLevelView',
]
