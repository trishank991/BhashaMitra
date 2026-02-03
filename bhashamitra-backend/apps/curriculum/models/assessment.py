"""Assessment and certificate models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Assessment(TimeStampedModel):
    """Formal assessment/test."""

    class AssessmentType(models.TextChoices):
        PLACEMENT = 'PLACEMENT', 'Placement Test'
        LEVEL_UP = 'LEVEL_UP', 'Level-Up Test'
        MODULE = 'MODULE', 'Module Completion'
        SKILL = 'SKILL', 'Skill Assessment'
        PRACTICE = 'PRACTICE', 'Practice Test'

    name = models.CharField(max_length=200)
    description = models.TextField()
    assessment_type = models.CharField(max_length=20, choices=AssessmentType.choices)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    passing_score = models.IntegerField(default=70)
    time_limit_minutes = models.IntegerField(default=30)
    questions_count = models.IntegerField(default=20)
    randomize_questions = models.BooleanField(default=True)
    show_correct_answers = models.BooleanField(default=True)
    allow_retake = models.BooleanField(default=True)
    retake_cooldown_hours = models.IntegerField(default=24)
    required_level = models.IntegerField(null=True, blank=True)
    prerequisite_assessment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'assessments'
        ordering = ['level', 'name']


class AssessmentQuestion(TimeStampedModel):
    """Assessment question."""

    class QuestionType(models.TextChoices):
        MULTIPLE_CHOICE = 'MC', 'Multiple Choice'
        TRUE_FALSE = 'TF', 'True/False'
        FILL_BLANK = 'FB', 'Fill in the Blank'
        MATCHING = 'MA', 'Matching'
        REORDER = 'RO', 'Reorder'
        LISTENING = 'LI', 'Listening'

    class SkillTested(models.TextChoices):
        READING = 'READING', 'Reading'
        WRITING = 'WRITING', 'Writing'
        LISTENING = 'LISTENING', 'Listening'
        GRAMMAR = 'GRAMMAR', 'Grammar'
        VOCABULARY = 'VOCABULARY', 'Vocabulary'
        ALPHABET = 'ALPHABET', 'Alphabet'

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_type = models.CharField(max_length=20, choices=QuestionType.choices)
    skill_tested = models.CharField(max_length=20, choices=SkillTested.choices)
    question_text = models.TextField()
    correct_answer = models.TextField()
    acceptable_answers = models.JSONField(default=list)
    options = models.JSONField(default=list)
    points = models.IntegerField(default=5)
    explanation = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'assessment_questions'
        ordering = ['order']

    def check_answer(self, user_answer: str) -> dict:
        user_clean = user_answer.strip().lower()
        correct_clean = self.correct_answer.strip().lower()
        acceptable = [a.lower() for a in self.acceptable_answers]
        is_correct = user_clean == correct_clean or user_clean in acceptable
        return {
            'is_correct': is_correct,
            'points': self.points if is_correct else 0,
            'correct_answer': self.correct_answer,
            'explanation': self.explanation,
        }


class AssessmentAttempt(TimeStampedModel):
    """Record of taking an assessment."""

    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    max_score = models.IntegerField(default=0)
    percentage = models.FloatField(default=0)
    passed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_taken_seconds = models.IntegerField(default=0)
    answers = models.JSONField(default=dict)
    skill_breakdown = models.JSONField(default=dict)

    class Meta:
        db_table = 'assessment_attempts'
        ordering = ['-started_at']


class Certificate(TimeStampedModel):
    """Achievement certificate."""

    class CertificateType(models.TextChoices):
        LEVEL_COMPLETION = 'LEVEL', 'Level Completion'
        MODULE_COMPLETION = 'MODULE', 'Module Completion'
        ACHIEVEMENT = 'ACHIEVEMENT', 'Achievement'

    certificate_id = models.CharField(max_length=20, unique=True, editable=False)
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='certificates')
    certificate_type = models.CharField(max_length=20, choices=CertificateType.choices)
    title = models.CharField(max_length=200)
    description = models.TextField()
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(null=True, blank=True)
    assessment_attempt = models.ForeignKey(AssessmentAttempt, on_delete=models.SET_NULL, null=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    pdf_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'certificates'
        ordering = ['-issued_at']

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            import secrets
            self.certificate_id = f"PA-{secrets.token_hex(4).upper()}"
        super().save(*args, **kwargs)
