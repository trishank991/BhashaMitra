"""Grammar models for structured language learning."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class GrammarTopic(TimeStampedModel):
    """Grammar concept/topic."""

    language = models.CharField(max_length=20, choices=Child.Language.choices)
    name = models.CharField(max_length=200)
    name_native = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    description_simple = models.TextField(blank=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'grammar_topics'
        ordering = ['level', 'order']


class GrammarRule(TimeStampedModel):
    """Specific grammar rule within a topic."""

    topic = models.ForeignKey(GrammarTopic, on_delete=models.CASCADE, related_name='rules')
    title = models.CharField(max_length=300)
    explanation = models.TextField()
    explanation_simple = models.TextField(blank=True)
    formula = models.CharField(max_length=500, blank=True)
    examples = models.JSONField(default=list)
    exceptions = models.JSONField(default=list)
    tips = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'grammar_rules'
        ordering = ['order']


class GrammarExercise(TimeStampedModel):
    """Exercise to practice grammar."""

    class ExerciseType(models.TextChoices):
        FILL_BLANK = 'FILL_BLANK', 'Fill in the Blank'
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        REORDER = 'REORDER', 'Reorder Words'
        TRANSLATE = 'TRANSLATE', 'Translate'
        ERROR_CORRECTION = 'ERROR', 'Find the Error'
        CONJUGATE = 'CONJUGATE', 'Conjugate Verb'
        MATCH = 'MATCH', 'Matching'
        TRUE_FALSE = 'TF', 'True/False'

    rule = models.ForeignKey(GrammarRule, on_delete=models.CASCADE, related_name='exercises')
    exercise_type = models.CharField(max_length=20, choices=ExerciseType.choices)
    question = models.TextField()
    correct_answer = models.TextField()
    acceptable_answers = models.JSONField(default=list)
    options = models.JSONField(default=list)
    hint = models.TextField(blank=True)
    explanation = models.TextField(blank=True)
    difficulty = models.IntegerField(default=1)
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'grammar_exercises'
        ordering = ['order']

    def check_answer(self, user_answer: str) -> dict:
        user_clean = user_answer.strip().lower()
        correct_clean = self.correct_answer.strip().lower()
        acceptable = [a.lower() for a in self.acceptable_answers]
        is_correct = user_clean == correct_clean or user_clean in acceptable
        return {
            'is_correct': is_correct,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
            'points': self.points if is_correct else 0,
        }


class GrammarProgress(TimeStampedModel):
    """Track child's grammar progress."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='grammar_progress')
    topic = models.ForeignKey(GrammarTopic, on_delete=models.CASCADE, related_name='progress_records')
    exercises_attempted = models.IntegerField(default=0)
    exercises_correct = models.IntegerField(default=0)
    mastered = models.BooleanField(default=False)
    mastered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'grammar_progress'
        unique_together = ['child', 'topic']

    @property
    def accuracy(self) -> float:
        return (self.exercises_correct / self.exercises_attempted * 100) if self.exercises_attempted else 0.0
