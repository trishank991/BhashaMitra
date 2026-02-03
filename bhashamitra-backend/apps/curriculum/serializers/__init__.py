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
from .level import (
    CurriculumLevelSerializer,
    CurriculumLevelDetailSerializer,
    CurriculumModuleSerializer,
    CurriculumModuleDetailSerializer,
    LessonSerializer,
    LessonDetailSerializer,
    LessonContentSerializer,
    LevelProgressSerializer,
    ModuleProgressSerializer,
    LessonProgressSerializer,
    LessonProgressUpdateSerializer,
)
from .songs import SongSerializer, SongListSerializer
from .peppi import (
    PeppiPersonalitySerializer,
    PeppiLearningContextSerializer,
    PeppiGreetingRequestSerializer,
    PeppiTeachWordRequestSerializer,
    PeppiFeedbackRequestSerializer,
)
from .teacher import TeacherSerializer, TeacherDetailSerializer
from .classroom import ClassroomSerializer, ClassroomDetailSerializer

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
    # Curriculum Hierarchy
    'CurriculumLevelSerializer',
    'CurriculumLevelDetailSerializer',
    'CurriculumModuleSerializer',
    'CurriculumModuleDetailSerializer',
    'LessonSerializer',
    'LessonDetailSerializer',
    'LessonContentSerializer',
    'LevelProgressSerializer',
    'ModuleProgressSerializer',
    'LessonProgressSerializer',
    'LessonProgressUpdateSerializer',
    # Songs
    'SongSerializer',
    'SongListSerializer',
    # Peppi
    'PeppiPersonalitySerializer',
    'PeppiLearningContextSerializer',
    'PeppiGreetingRequestSerializer',
    'PeppiTeachWordRequestSerializer',
    'PeppiFeedbackRequestSerializer',
    # Teacher & Classroom
    'TeacherSerializer',
    'TeacherDetailSerializer',
    'ClassroomSerializer',
    'ClassroomDetailSerializer',
]
