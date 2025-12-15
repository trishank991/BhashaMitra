"""Curriculum serializers."""
from .script import (
    ScriptSerializer,
    ScriptDetailSerializer,
    AlphabetCategorySerializer,
    LetterSerializer,
    LetterDetailSerializer,
    MatraSerializer,
    LetterProgressSerializer,
)
from .vocabulary import (
    VocabularyThemeSerializer,
    VocabularyThemeDetailSerializer,
    VocabularyWordSerializer,
    VocabularyWordDetailSerializer,
    WordProgressSerializer,
    FlashcardSerializer,
)
from .grammar import (
    GrammarTopicSerializer,
    GrammarTopicDetailSerializer,
    GrammarRuleSerializer,
    GrammarExerciseSerializer,
    GrammarProgressSerializer,
)
from .games import (
    GameSerializer,
    GameDetailSerializer,
    GameSessionSerializer,
    GameLeaderboardSerializer,
)
from .assessment import (
    AssessmentSerializer,
    AssessmentDetailSerializer,
    AssessmentQuestionSerializer,
    AssessmentAttemptSerializer,
    CertificateSerializer,
)

__all__ = [
    # Script
    'ScriptSerializer',
    'ScriptDetailSerializer',
    'AlphabetCategorySerializer',
    'LetterSerializer',
    'LetterDetailSerializer',
    'MatraSerializer',
    'LetterProgressSerializer',
    # Vocabulary
    'VocabularyThemeSerializer',
    'VocabularyThemeDetailSerializer',
    'VocabularyWordSerializer',
    'VocabularyWordDetailSerializer',
    'WordProgressSerializer',
    'FlashcardSerializer',
    # Grammar
    'GrammarTopicSerializer',
    'GrammarTopicDetailSerializer',
    'GrammarRuleSerializer',
    'GrammarExerciseSerializer',
    'GrammarProgressSerializer',
    # Games
    'GameSerializer',
    'GameDetailSerializer',
    'GameSessionSerializer',
    'GameLeaderboardSerializer',
    # Assessment
    'AssessmentSerializer',
    'AssessmentDetailSerializer',
    'AssessmentQuestionSerializer',
    'AssessmentAttemptSerializer',
    'CertificateSerializer',
]
