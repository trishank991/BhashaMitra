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
]
