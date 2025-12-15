# BhashaMitra Implementation Guide - Part 3: Curriculum Module

> **Part 3**: Curriculum Module (Alphabets, Vocabulary, Grammar, Games, Assessments)
> **Builds on**: Part 1 (Core/Auth/Children) & Part 2 (Stories/Progress/Gamification/Speech)
> **Models**: 22 new models | **Seed Data**: Hindi alphabet, vocabulary, badges

---

## Table of Contents

1. [Script & Alphabet Module](#1-script--alphabet-module)
2. [Vocabulary Module with SRS](#2-vocabulary-module-with-srs)
3. [Grammar Module](#3-grammar-module)
4. [Games Module](#4-games-module)
5. [Assessment & Certificates](#5-assessment--certificates)
6. [Seed Scripts](#6-seed-scripts)
7. [URL Configuration](#7-url-configuration)
8. [Services Layer](#8-services-layer)

---

## 1. Script & Alphabet Module

### apps/curriculum/models/script.py

\`\`\`python
"""Script and alphabet models for Devanagari, Tamil, etc."""
import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Script(TimeStampedModel):
    """Writing system for a language (e.g., Devanagari for Hindi)."""
    
    language = models.CharField(max_length=20, choices=Child.Language.choices, unique=True)
    name = models.CharField(max_length=50)
    name_native = models.CharField(max_length=100)
    description = models.TextField()
    total_letters = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'scripts'
    
    def __str__(self):
        return f"{self.name} ({self.language})"


class AlphabetCategory(TimeStampedModel):
    """Category of letters (vowels, consonants, matras, etc.)."""
    
    class CategoryType(models.TextChoices):
        VOWEL = 'VOWEL', 'Vowel'
        CONSONANT = 'CONSONANT', 'Consonant'
        MATRA = 'MATRA', 'Matra (Vowel Mark)'
        CONJUNCT = 'CONJUNCT', 'Conjunct'
        NUMBER = 'NUMBER', 'Number'
        SPECIAL = 'SPECIAL', 'Special Character'
    
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=50)
    name_native = models.CharField(max_length=100, blank=True)
    category_type = models.CharField(max_length=20, choices=CategoryType.choices)
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'alphabet_categories'
        ordering = ['order']
        unique_together = ['script', 'category_type']


class Letter(TimeStampedModel):
    """Individual letter/character in the script."""
    
    category = models.ForeignKey(AlphabetCategory, on_delete=models.CASCADE, related_name='letters')
    character = models.CharField(max_length=10)
    romanization = models.CharField(max_length=20)
    ipa = models.CharField(max_length=50, blank=True)
    pronunciation_guide = models.TextField(blank=True)
    audio_url = models.URLField(blank=True, null=True)
    stroke_order_url = models.URLField(blank=True, null=True)
    example_word = models.CharField(max_length=100, blank=True)
    example_word_romanization = models.CharField(max_length=100, blank=True)
    example_word_translation = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'letters'
        ordering = ['order']
        unique_together = ['category', 'character']


class Matra(TimeStampedModel):
    """Vowel marks that modify consonants."""
    
    script = models.ForeignKey(Script, on_delete=models.CASCADE, related_name='matras')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    example_with_ka = models.CharField(max_length=20)
    audio_url = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'matras'
        ordering = ['order']


class LetterProgress(TimeStampedModel):
    """Track child's progress on each letter."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='letter_progress')
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name='progress_records')
    recognition_score = models.IntegerField(default=0)
    listening_score = models.IntegerField(default=0)
    tracing_score = models.IntegerField(default=0)
    writing_score = models.IntegerField(default=0)
    pronunciation_score = models.IntegerField(default=0)
    times_practiced = models.IntegerField(default=0)
    mastered = models.BooleanField(default=False)
    mastered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'letter_progress'
        unique_together = ['child', 'letter']
    
    @property
    def overall_score(self) -> int:
        scores = [self.recognition_score, self.listening_score, 
                  self.tracing_score, self.writing_score, self.pronunciation_score]
        return sum(scores) // len(scores)
    
    def check_mastery(self) -> bool:
        from django.utils import timezone
        if not self.mastered and self.overall_score >= 80 and self.times_practiced >= 5:
            self.mastered = True
            self.mastered_at = timezone.now()
            self.save()
            return True
        return False
\`\`\`

---

## 2. Vocabulary Module with SRS

### apps/curriculum/models/vocabulary.py

\`\`\`python
"""Vocabulary models with spaced repetition system (SM-2 algorithm)."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from datetime import timedelta
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class VocabularyTheme(TimeStampedModel):
    """Thematic vocabulary groups (e.g., Family, Colors, Animals)."""
    
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    name = models.CharField(max_length=100)
    name_native = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    order = models.IntegerField(default=0)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'vocabulary_themes'
        ordering = ['level', 'order']
        unique_together = ['language', 'name']
    
    @property
    def word_count(self):
        return self.words.count()


class VocabularyWord(TimeStampedModel):
    """Individual vocabulary word."""
    
    class PartOfSpeech(models.TextChoices):
        NOUN = 'NOUN', 'Noun'
        VERB = 'VERB', 'Verb'
        ADJECTIVE = 'ADJECTIVE', 'Adjective'
        ADVERB = 'ADVERB', 'Adverb'
        PRONOUN = 'PRONOUN', 'Pronoun'
        NUMBER = 'NUMBER', 'Number'
        OTHER = 'OTHER', 'Other'
    
    class Gender(models.TextChoices):
        MASCULINE = 'M', 'Masculine'
        FEMININE = 'F', 'Feminine'
        NEUTER = 'N', 'Neuter'
        NONE = 'NONE', 'Not Applicable'
    
    theme = models.ForeignKey(VocabularyTheme, on_delete=models.CASCADE, related_name='words')
    word = models.CharField(max_length=200)
    romanization = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    part_of_speech = models.CharField(max_length=20, choices=PartOfSpeech.choices, default='NOUN')
    gender = models.CharField(max_length=10, choices=Gender.choices, default='NONE')
    pronunciation_audio_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    example_sentence = models.TextField(blank=True)
    difficulty = models.IntegerField(default=1)
    order = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'vocabulary_words'
        ordering = ['order']
        unique_together = ['theme', 'word']


class WordProgress(TimeStampedModel):
    """Track child's progress with SM-2 SRS algorithm."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='word_progress')
    word = models.ForeignKey(VocabularyWord, on_delete=models.CASCADE, related_name='progress_records')
    
    # SM-2 SRS fields
    ease_factor = models.FloatField(default=2.5)
    interval_days = models.IntegerField(default=1)
    repetitions = models.IntegerField(default=0)
    next_review = models.DateTimeField(default=timezone.now)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    
    # Stats
    times_reviewed = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    mastered = models.BooleanField(default=False)
    mastered_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'word_progress'
        unique_together = ['child', 'word']
    
    def update_srs(self, quality: int):
        """
        Update SRS using SM-2 algorithm.
        quality: 0-5 (0=blackout, 3=correct with difficulty, 5=perfect)
        """
        self.times_reviewed += 1
        self.last_reviewed = timezone.now()
        
        if quality >= 3:
            self.times_correct += 1
            if self.repetitions == 0:
                self.interval_days = 1
            elif self.repetitions == 1:
                self.interval_days = 6
            else:
                self.interval_days = int(self.interval_days * self.ease_factor)
            self.repetitions += 1
        else:
            self.repetitions = 0
            self.interval_days = 1
        
        # Update ease factor (min 1.3)
        self.ease_factor = max(1.3, self.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        self.next_review = timezone.now() + timedelta(days=self.interval_days)
        self.save()
        
        # Check mastery
        if self.interval_days > 21 and self.times_reviewed >= 5:
            accuracy = (self.times_correct / self.times_reviewed) * 100
            if accuracy >= 90 and not self.mastered:
                self.mastered = True
                self.mastered_at = timezone.now()
                self.save()
    
    @property
    def accuracy(self) -> float:
        return (self.times_correct / self.times_reviewed * 100) if self.times_reviewed else 0.0
\`\`\`

---

## 3. Grammar Module

### apps/curriculum/models/grammar.py

\`\`\`python
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
\`\`\`

---

## 4. Games Module

### apps/curriculum/models/games.py

\`\`\`python
"""Educational games models."""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.children.models import Child


class Game(TimeStampedModel):
    """Educational game definition."""
    
    class GameType(models.TextChoices):
        MEMORY = 'MEMORY', 'Memory Match'
        WORDSEARCH = 'WORDSEARCH', 'Word Search'
        HANGMAN = 'HANGMAN', 'Hangman'
        QUIZ = 'QUIZ', 'Quiz Challenge'
        DRAGDROP = 'DRAGDROP', 'Drag and Drop'
        LISTENING = 'LISTENING', 'Listening Challenge'
        SPEED = 'SPEED', 'Speed Round'
        BUILDER = 'BUILDER', 'Word Builder'
        JUMBLE = 'JUMBLE', 'Sentence Jumble'
        PICTURE = 'PICTURE', 'Picture Match'
    
    class SkillFocus(models.TextChoices):
        ALPHABET = 'ALPHABET', 'Alphabet Recognition'
        VOCABULARY = 'VOCAB', 'Vocabulary'
        GRAMMAR = 'GRAMMAR', 'Grammar'
        LISTENING = 'LISTENING', 'Listening'
        READING = 'READING', 'Reading'
        SPELLING = 'SPELLING', 'Spelling'
        MIXED = 'MIXED', 'Mixed Skills'
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField()
    game_type = models.CharField(max_length=20, choices=GameType.choices)
    skill_focus = models.CharField(max_length=20, choices=SkillFocus.choices)
    language = models.CharField(max_length=20, choices=Child.Language.choices)
    level = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    duration_seconds = models.IntegerField(default=300)
    questions_per_round = models.IntegerField(default=10)
    lives = models.IntegerField(default=3)
    points_per_correct = models.IntegerField(default=10)
    bonus_completion = models.IntegerField(default=50)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'games'
        ordering = ['level', 'name']


class GameSession(TimeStampedModel):
    """Record of a game play session."""
    
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='game_sessions')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='sessions')
    score = models.IntegerField(default=0)
    questions_attempted = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    lives_remaining = models.IntegerField(default=0)
    points_earned = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'game_sessions'
    
    @property
    def accuracy(self) -> float:
        return (self.questions_correct / self.questions_attempted * 100) if self.questions_attempted else 0.0


class GameLeaderboard(TimeStampedModel):
    """Leaderboard entries."""
    
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='leaderboard')
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='leaderboard_entries')
    high_score = models.IntegerField(default=0)
    best_accuracy = models.FloatField(default=0)
    games_played = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'game_leaderboard'
        unique_together = ['game', 'child']
        ordering = ['-high_score']
    
    def update_from_session(self, session: GameSession):
        self.games_played += 1
        if session.score > self.high_score:
            self.high_score = session.score
        if session.accuracy > self.best_accuracy:
            self.best_accuracy = session.accuracy
        self.save()
\`\`\`

---

## 5. Assessment & Certificates

### apps/curriculum/models/assessment.py

\`\`\`python
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
            self.certificate_id = f"BM-{secrets.token_hex(4).upper()}"
        super().save(*args, **kwargs)
\`\`\`

---

## 6. Seed Scripts

### scripts/seed_badges.py

\`\`\`python
"""Seed badges for gamification."""
import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.gamification.models import Badge

BADGES = [
    {'name': 'First Story', 'description': 'Complete your first story!', 'icon': 'book-open', 
     'criteria_type': 'STORIES_COMPLETED', 'criteria_value': 1, 'display_order': 1},
    {'name': 'Story Explorer', 'description': 'Complete 5 stories', 'icon': 'book-marked', 
     'criteria_type': 'STORIES_COMPLETED', 'criteria_value': 5, 'display_order': 2},
    {'name': 'Bookworm', 'description': 'Complete 10 stories', 'icon': 'library', 
     'criteria_type': 'STORIES_COMPLETED', 'criteria_value': 10, 'display_order': 3},
    {'name': 'Story Master', 'description': 'Complete 25 stories', 'icon': 'crown', 
     'criteria_type': 'STORIES_COMPLETED', 'criteria_value': 25, 'display_order': 4},
    {'name': 'Getting Started', 'description': 'Practice 3 days in a row', 'icon': 'flame', 
     'criteria_type': 'STREAK_DAYS', 'criteria_value': 3, 'display_order': 10},
    {'name': 'Week Warrior', 'description': 'Practice 7 days in a row', 'icon': 'fire', 
     'criteria_type': 'STREAK_DAYS', 'criteria_value': 7, 'display_order': 11},
    {'name': 'Month Master', 'description': 'Practice 30 days in a row', 'icon': 'trophy', 
     'criteria_type': 'STREAK_DAYS', 'criteria_value': 30, 'display_order': 13},
    {'name': 'First Words', 'description': 'Record your first voice recording', 'icon': 'mic', 
     'criteria_type': 'VOICE_RECORDINGS', 'criteria_value': 1, 'display_order': 20},
    {'name': 'Voice Star', 'description': 'Make 10 voice recordings', 'icon': 'mic-vocal', 
     'criteria_type': 'VOICE_RECORDINGS', 'criteria_value': 10, 'display_order': 21},
    {'name': 'Point Collector', 'description': 'Earn 100 points', 'icon': 'coins', 
     'criteria_type': 'POINTS_EARNED', 'criteria_value': 100, 'display_order': 30},
    {'name': 'Point Hunter', 'description': 'Earn 500 points', 'icon': 'gem', 
     'criteria_type': 'POINTS_EARNED', 'criteria_value': 500, 'display_order': 31},
    {'name': 'Point Champion', 'description': 'Earn 1000 points', 'icon': 'diamond', 
     'criteria_type': 'POINTS_EARNED', 'criteria_value': 1000, 'display_order': 32},
]

def seed_badges():
    for badge_data in BADGES:
        Badge.objects.update_or_create(name=badge_data['name'], defaults=badge_data)
    print(f"✓ Seeded {len(BADGES)} badges")

if __name__ == '__main__':
    seed_badges()
\`\`\`
update_or_create(
        script=script, category_type='CONSONANT',
        defaults={'name': 'Consonants', 'name_native': 'व्यंजन', 'order': 2}
    )
    
    for i, v in enumerate(VOWELS):
        Letter.objects.update_or_create(
            category=vowel_cat, character=v['char'],
            defaults={'romanization': v['roman'], 'ipa': v['ipa'], 'example_word': v['example'],
                      'example_word_romanization': v['ex_roman'], 'example_word_translation': v['ex_trans'], 'order': i+1}
        )
    
    for i, c in enumerate(CONSONANTS):
        Letter.objects.update_or_create(
            category=consonant_cat, character=c['char'],
            defaults={'romanization': c['roman'], 'ipa': c['ipa'], 'example_word': c['example'],
                      'example_word_romanization': c['ex_roman'], 'example_word_translation': c['ex_trans'], 'order': i+1}
        )
    
    for i, m in enumerate(MATRAS):
        Matra.objects.update_or_create(
            script=script, symbol=m['symbol'],
            defaults={'name': m['name'], 'example_with_ka': m['example_ka'], 'order': i+1}
        )
    
    print(f"✓ Hindi alphabet: {len(VOWELS)} vowels, {len(CONSONANTS)} consonants, {len(MATRAS)} matras")

if __name__ == '__main__':
    seed_hindi_alphabet()
\`\`\`

### scripts/seed_vocabulary_themes.py

\`\`\`python
"""Seed vocabulary themes and words."""
import os, sys, django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.curriculum.models.vocabulary import VocabularyTheme, VocabularyWord

THEMES = [
    {
        'language': 'HINDI', 'name': 'Family', 'name_native': 'परिवार', 'icon': 'users', 'level': 1, 'order': 1,
        'words': [
            {'word': 'माँ', 'roman': 'maa', 'trans': 'mother', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'पिता', 'roman': 'pita', 'trans': 'father', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'भाई', 'roman': 'bhai', 'trans': 'brother', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'बहन', 'roman': 'bahan', 'trans': 'sister', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'दादा', 'roman': 'dada', 'trans': 'grandfather (paternal)', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'दादी', 'roman': 'dadi', 'trans': 'grandmother (paternal)', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'नाना', 'roman': 'nana', 'trans': 'grandfather (maternal)', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'नानी', 'roman': 'nani', 'trans': 'grandmother (maternal)', 'pos': 'NOUN', 'gender': 'F'},
        ]
    },
    {
        'language': 'HINDI', 'name': 'Colors', 'name_native': 'रंग', 'icon': 'palette', 'level': 1, 'order': 2,
        'words': [
            {'word': 'लाल', 'roman': 'laal', 'trans': 'red', 'pos': 'ADJECTIVE', 'gender': 'NONE'},
            {'word': 'नीला', 'roman': 'neela', 'trans': 'blue', 'pos': 'ADJECTIVE', 'gender': 'M'},
            {'word': 'पीला', 'roman': 'peela', 'trans': 'yellow', 'pos': 'ADJECTIVE', 'gender': 'M'},
            {'word': 'हरा', 'roman': 'hara', 'trans': 'green', 'pos': 'ADJECTIVE', 'gender': 'M'},
            {'word': 'काला', 'roman': 'kaala', 'trans': 'black', 'pos': 'ADJECTIVE', 'gender': 'M'},
            {'word': 'सफ़ेद', 'roman': 'safed', 'trans': 'white', 'pos': 'ADJECTIVE', 'gender': 'NONE'},
            {'word': 'नारंगी', 'roman': 'narangi', 'trans': 'orange', 'pos': 'ADJECTIVE', 'gender': 'NONE'},
            {'word': 'गुलाबी', 'roman': 'gulaabi', 'trans': 'pink', 'pos': 'ADJECTIVE', 'gender': 'NONE'},
        ]
    },
    {
        'language': 'HINDI', 'name': 'Numbers', 'name_native': 'संख्याएँ', 'icon': 'hash', 'level': 1, 'order': 3,
        'words': [
            {'word': 'एक', 'roman': 'ek', 'trans': 'one', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'दो', 'roman': 'do', 'trans': 'two', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'तीन', 'roman': 'teen', 'trans': 'three', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'चार', 'roman': 'chaar', 'trans': 'four', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'पाँच', 'roman': 'paanch', 'trans': 'five', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'छह', 'roman': 'chhah', 'trans': 'six', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'सात', 'roman': 'saat', 'trans': 'seven', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'आठ', 'roman': 'aath', 'trans': 'eight', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'नौ', 'roman': 'nau', 'trans': 'nine', 'pos': 'NUMBER', 'gender': 'NONE'},
            {'word': 'दस', 'roman': 'das', 'trans': 'ten', 'pos': 'NUMBER', 'gender': 'NONE'},
        ]
    },
    {
        'language': 'HINDI', 'name': 'Animals', 'name_native': 'जानवर', 'icon': 'paw-print', 'level': 1, 'order': 4,
        'words': [
            {'word': 'कुत्ता', 'roman': 'kutta', 'trans': 'dog', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'बिल्ली', 'roman': 'billi', 'trans': 'cat', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'गाय', 'roman': 'gaay', 'trans': 'cow', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'घोड़ा', 'roman': 'ghoda', 'trans': 'horse', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'हाथी', 'roman': 'haathi', 'trans': 'elephant', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'शेर', 'roman': 'sher', 'trans': 'lion', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'बंदर', 'roman': 'bandar', 'trans': 'monkey', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'चिड़िया', 'roman': 'chidiya', 'trans': 'bird', 'pos': 'NOUN', 'gender': 'F'},
        ]
    },
    {
        'language': 'HINDI', 'name': 'Food', 'name_native': 'खाना', 'icon': 'utensils', 'level': 1, 'order': 5,
        'words': [
            {'word': 'रोटी', 'roman': 'roti', 'trans': 'bread', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'चावल', 'roman': 'chaawal', 'trans': 'rice', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'दाल', 'roman': 'daal', 'trans': 'lentils', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'सब्ज़ी', 'roman': 'sabzi', 'trans': 'vegetable', 'pos': 'NOUN', 'gender': 'F'},
            {'word': 'दूध', 'roman': 'doodh', 'trans': 'milk', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'पानी', 'roman': 'paani', 'trans': 'water', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'फल', 'roman': 'phal', 'trans': 'fruit', 'pos': 'NOUN', 'gender': 'M'},
            {'word': 'मिठाई', 'roman': 'mithai', 'trans': 'sweets', 'pos': 'NOUN', 'gender': 'F'},
        ]
    },
]

def seed_vocabulary():
    total_words = 0
    for theme_data in THEMES:
        words = theme_data.pop('words')
        theme, _ = VocabularyTheme.objects.update_or_create(
            language=theme_data['language'], name=theme_data['name'], defaults=theme_data
        )
        for i, w in enumerate(words):
            VocabularyWord.objects.update_or_create(
                theme=theme, word=w['word'],
                defaults={'romanization': w['roman'], 'translation': w['trans'],
                          'part_of_speech': w['pos'], 'gender': w['gender'], 'order': i+1, 'difficulty': 1}
            )
            total_words += 1
    print(f"✓ Vocabulary: {len(THEMES)} themes, {total_words} words")

if __name__ == '__main__':
    seed_vocabulary()
\`\`\`

---

## 7. URL Configuration

### apps/curriculum/urls.py

\`\`\`python
"""Curriculum URL configuration."""
from django.urls import path
from . import views

app_name = 'curriculum'

urlpatterns = [
    # Alphabet
    path('alphabet/scripts/', views.ScriptListView.as_view(), name='script-list'),
    path('alphabet/scripts/<uuid:pk>/', views.ScriptDetailView.as_view(), name='script-detail'),
    path('alphabet/scripts/<uuid:pk>/letters/', views.ScriptLettersView.as_view(), name='script-letters'),
    path('alphabet/letters/', views.LetterListView.as_view(), name='letter-list'),
    path('alphabet/letters/<uuid:pk>/', views.LetterDetailView.as_view(), name='letter-detail'),
    path('alphabet/letters/<uuid:pk>/progress/', views.LetterProgressView.as_view(), name='letter-progress'),
    path('alphabet/progress/', views.AlphabetProgressView.as_view(), name='alphabet-progress'),
    
    # Vocabulary
    path('vocabulary/themes/', views.VocabularyThemeListView.as_view(), name='theme-list'),
    path('vocabulary/themes/<uuid:pk>/', views.ThemeDetailView.as_view(), name='theme-detail'),
    path('vocabulary/themes/<uuid:pk>/words/', views.ThemeWordsView.as_view(), name='theme-words'),
    path('vocabulary/themes/<uuid:pk>/stats/', views.ThemeStatsView.as_view(), name='theme-stats'),
    path('vocabulary/words/<uuid:pk>/', views.WordDetailView.as_view(), name='word-detail'),
    path('vocabulary/flashcards/due/', views.FlashcardsDueView.as_view(), name='flashcards-due'),
    path('vocabulary/flashcards/review/', views.FlashcardReviewView.as_view(), name='flashcard-review'),
    path('vocabulary/flashcards/session/', views.FlashcardSessionView.as_view(), name='flashcard-session'),
    
    # Grammar
    path('grammar/topics/', views.GrammarTopicListView.as_view(), name='topic-list'),
    path('grammar/topics/<uuid:pk>/', views.GrammarTopicDetailView.as_view(), name='topic-detail'),
    path('grammar/topics/<uuid:pk>/rules/', views.TopicRulesView.as_view(), name='topic-rules'),
    path('grammar/topics/<uuid:pk>/exercises/', views.TopicExercisesView.as_view(), name='topic-exercises'),
    path('grammar/exercises/<uuid:pk>/', views.ExerciseDetailView.as_view(), name='exercise-detail'),
    path('grammar/exercises/<uuid:pk>/submit/', views.ExerciseSubmitView.as_view(), name='exercise-submit'),
    path('grammar/progress/', views.GrammarProgressView.as_view(), name='grammar-progress'),
    
    # Games
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('games/<uuid:pk>/', views.GameDetailView.as_view(), name='game-detail'),
    path('games/<uuid:pk>/start/', views.GameStartView.as_view(), name='game-start'),
    path('games/<uuid:pk>/submit/', views.GameSubmitView.as_view(), name='game-submit'),
    path('games/<uuid:pk>/leaderboard/', views.GameLeaderboardView.as_view(), name='game-leaderboard'),
    path('games/leaderboard/', views.GlobalLeaderboardView.as_view(), name='global-leaderboard'),
    path('games/history/', views.GameHistoryView.as_view(), name='game-history'),
    
    # Assessments
    path('assessments/', views.AssessmentListView.as_view(), name='assessment-list'),
    path('assessments/<uuid:pk>/', views.AssessmentDetailView.as_view(), name='assessment-detail'),
    path('assessments/<uuid:pk>/start/', views.AssessmentStartView.as_view(), name='assessment-start'),
    path('assessments/<uuid:pk>/submit/', views.AssessmentSubmitView.as_view(), name='assessment-submit'),
    path('assessments/attempts/', views.AssessmentAttemptsView.as_view(), name='assessment-attempts'),
    path('assessments/attempts/<uuid:pk>/', views.AttemptDetailView.as_view(), name='attempt-detail'),
    path('assessments/certificates/', views.CertificateListView.as_view(), name='certificate-list'),
    path('assessments/certificates/<str:certificate_id>/', views.CertificateDetailView.as_view(), name='certificate-detail'),
]
\`\`\`

### config/urls.py (updated)

\`\`\`python
"""Main URL configuration with curriculum routes."""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # API v1
    path('api/v1/auth/', include('apps.users.urls', namespace='auth')),
    path('api/v1/children/', include('apps.children.urls', namespace='children')),
    path('api/v1/stories/', include('apps.stories.urls', namespace='stories')),
    path('api/v1/speech/', include('apps.speech.urls', namespace='speech')),
    
    # Curriculum (nested under children)
    path('api/v1/children/<uuid:child_id>/curriculum/', include('apps.curriculum.urls', namespace='curriculum')),
]
\`\`\`

---

## 8. Services Layer

### apps/curriculum/services/srs_service.py

\`\`\`python
"""Spaced Repetition Service using SM-2 algorithm."""
from django.utils import timezone
from typing import List, Optional
from apps.curriculum.models.vocabulary import VocabularyWord, WordProgress, VocabularyTheme


class SRSService:
    """Service for managing spaced repetition vocabulary learning."""
    
    @staticmethod
    def get_due_words(child_id: str, theme_id: Optional[str] = None, limit: int = 20) -> List[WordProgress]:
        """Get words due for review based on SRS schedule."""
        queryset = WordProgress.objects.filter(
            child_id=child_id,
            next_review__lte=timezone.now(),
            mastered=False
        ).select_related('word', 'word__theme')
        
        if theme_id:
            queryset = queryset.filter(word__theme_id=theme_id)
        
        return list(queryset.order_by('next_review')[:limit])
    
    @staticmethod
    def get_new_words(child_id: str, theme_id: str, limit: int = 5) -> List[VocabularyWord]:
        """Get new words not yet started by the child."""
        started_word_ids = WordProgress.objects.filter(
            child_id=child_id
        ).values_list('word_id', flat=True)
        
        return list(
            VocabularyWord.objects.filter(theme_id=theme_id)
            .exclude(id__in=started_word_ids)
            .order_by('order')[:limit]
        )
    
    @staticmethod
    def start_word(child_id: str, word_id: str) -> WordProgress:
        """Initialize progress for a new word."""
        progress, created = WordProgress.objects.get_or_create(
            child_id=child_id,
            word_id=word_id,
            defaults={'next_review': timezone.now()}
        )
        return progress
    
    @staticmethod
    def record_review(child_id: str, word_id: str, quality: int) -> dict:
        """
        Record a review and update SRS schedule.
        
        Quality scale (SM-2):
        0 - Complete blackout
        1 - Incorrect, but recognized answer
        2 - Incorrect, but easy to recall
        3 - Correct with serious difficulty
        4 - Correct with some hesitation
        5 - Perfect recall
        """
        progress = WordProgress.objects.get(child_id=child_id, word_id=word_id)
        progress.update_srs(quality)
        
        return {
            'word_id': str(word_id),
            'quality': quality,
            'correct': quality >= 3,
            'new_interval_days': progress.interval_days,
            'next_review': progress.next_review.isoformat(),
            'ease_factor': round(progress.ease_factor, 2),
            'mastered': progress.mastered,
        }
    
    @staticmethod
    def get_theme_stats(child_id: str, theme_id: str) -> dict:
        """Get detailed learning statistics for a theme."""
        theme = VocabularyTheme.objects.get(id=theme_id)
        total_words = theme.words.count()
        
        progress_qs = WordProgress.objects.filter(
            child_id=child_id,
            word__theme_id=theme_id
        )
        
        words_started = progress_qs.count()
        words_mastered = progress_qs.filter(mastered=True).count()
        words_due = progress_qs.filter(
            next_review__lte=timezone.now(),
            mastered=False
        ).count()
        
        total_reviews = sum(p.times_reviewed for p in progress_qs)
        total_correct = sum(p.times_correct for p in progress_qs)
        
        return {
            'theme_id': str(theme_id),
            'theme_name': theme.name,
            'theme_name_native': theme.name_native,
            'total_words': total_words,
            'words_started': words_started,
            'words_mastered': words_mastered,
            'words_due': words_due,
            'words_remaining': total_words - words_started,
            'progress_percentage': round((words_mastered / total_words) * 100, 1) if total_words else 0,
            'total_reviews': total_reviews,
            'overall_accuracy': round((total_correct / total_reviews) * 100, 1) if total_reviews else 0,
        }
    
    @staticmethod
    def get_child_vocabulary_summary(child_id: str) -> dict:
        """Get overall vocabulary summary across all themes."""
        progress_qs = WordProgress.objects.filter(child_id=child_id)
        
        return {
            'total_words_started': progress_qs.count(),
            'total_words_mastered': progress_qs.filter(mastered=True).count(),
            'total_words_due': progress_qs.filter(
                next_review__lte=timezone.now(),
                mastered=False
            ).count(),
            'total_reviews': sum(p.times_reviewed for p in progress_qs),
        }
\`\`\`

### apps/curriculum/services/assessment_service.py

\`\`\`python
"""Assessment service for tests and certificates."""
from django.utils import timezone
from django.db import transaction
from datetime import timedelta
from typing import Tuple, List, Optional
from apps.curriculum.models.assessment import Assessment, AssessmentQuestion, AssessmentAttempt, Certificate
from apps.children.models import Child


class AssessmentService:
    """Service for managing assessments and certificates."""
    
    @staticmethod
    def can_take_assessment(child: Child, assessment: Assessment) -> Tuple[bool, str]:
        """Check if child is eligible to take an assessment."""
        # Check level requirement
        if assessment.required_level and child.level < assessment.required_level:
            return False, f"Requires level {assessment.required_level}. Current level: {child.level}"
        
        # Check prerequisite
        if assessment.prerequisite_assessment:
            passed = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment.prerequisite_assessment,
                passed=True
            ).exists()
            if not passed:
                return False, f"Must pass '{assessment.prerequisite_assessment.name}' first"
        
        # Check retake policy
        if not assessment.allow_retake:
            existing = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment
            ).exists()
            if existing:
                return False, "This assessment can only be taken once"
        
        # Check cooldown
        if assessment.retake_cooldown_hours > 0:
            cooldown_time = timezone.now() - timedelta(hours=assessment.retake_cooldown_hours)
            recent = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment,
                completed_at__gte=cooldown_time
            ).exists()
            if recent:
                return False, f"Must wait {assessment.retake_cooldown_hours} hours between attempts"
        
        return True, "Eligible"
    
    @staticmethod
    def start_assessment(child: Child, assessment: Assessment) -> AssessmentAttempt:
        """Start a new assessment attempt."""
        questions = assessment.questions.all()
        if assessment.randomize_questions:
            questions = questions.order_by('?')[:assessment.questions_count]
        
        max_score = sum(q.points for q in questions)
        
        attempt = AssessmentAttempt.objects.create(
            child=child,
            assessment=assessment,
            max_score=max_score
        )
        
        return attempt
    
    @staticmethod
    @transaction.atomic
    def submit_assessment(attempt: AssessmentAttempt, answers: dict) -> dict:
        """Grade and submit an assessment."""
        total_score = 0
        skill_scores = {}
        results = []
        
        for question in attempt.assessment.questions.all():
            q_id = str(question.id)
            user_answer = answers.get(q_id, "")
            result = question.check_answer(user_answer)
            
            results.append({
                'question_id': q_id,
                'user_answer': user_answer,
                'is_correct': result['is_correct'],
                'points': result['points'],
                'correct_answer': result['correct_answer'] if attempt.assessment.show_correct_answers else None,
            })
            
            total_score += result['points']
            
            # Track by skill
            skill = question.skill_tested
            if skill not in skill_scores:
                skill_scores[skill] = {'correct': 0, 'total': 0, 'points': 0, 'max_points': 0}
            skill_scores[skill]['total'] += 1
            skill_scores[skill]['max_points'] += question.points
            if result['is_correct']:
                skill_scores[skill]['correct'] += 1
                skill_scores[skill]['points'] += result['points']
        
        # Calculate percentage
        percentage = (total_score / attempt.max_score * 100) if attempt.max_score else 0
        passed = percentage >= attempt.assessment.passing_score
        
        # Update attempt
        attempt.score = total_score
        attempt.percentage = round(percentage, 1)
        attempt.passed = passed
        attempt.completed_at = timezone.now()
        attempt.time_taken_seconds = int((attempt.completed_at - attempt.started_at).total_seconds())
        attempt.answers = answers
        attempt.skill_breakdown = skill_scores
        attempt.save()
        
        # Generate certificate if passed level-up assessment
        certificate = None
        if passed and attempt.assessment.assessment_type == 'LEVEL_UP':
            certificate = AssessmentService.generate_certificate(attempt)
            # Level up the child
            if attempt.child.level < 5:
                attempt.child.level += 1
                attempt.child.save()
        
        return {
            'attempt_id': str(attempt.id),
            'score': total_score,
            'max_score': attempt.max_score,
            'percentage': attempt.percentage,
            'passed': passed,
            'passing_score': attempt.assessment.passing_score,
            'time_taken_seconds': attempt.time_taken_seconds,
            'skill_breakdown': skill_scores,
            'certificate_id': certificate.certificate_id if certificate else None,
            'results': results if attempt.assessment.show_correct_answers else None,
        }
    
    @staticmethod
    def generate_certificate(attempt: AssessmentAttempt) -> Certificate:
        """Generate a certificate for a passed assessment."""
        cert_type = 'LEVEL' if attempt.assessment.assessment_type == 'LEVEL_UP' else 'MODULE'
        
        return Certificate.objects.create(
            child=attempt.child,
            certificate_type=cert_type,
            title=f"Level {attempt.assessment.level} Achievement Certificate",
            description=f"Successfully completed {attempt.assessment.name} with {attempt.percentage}% score",
            language=attempt.assessment.language,
            level=attempt.assessment.level,
            assessment_attempt=attempt,
        )
    
    @staticmethod
    def get_available_assessments(child: Child, language: str) -> List[dict]:
        """Get list of assessments with availability status."""
        assessments = Assessment.objects.filter(
            language=language,
            is_active=True
        ).order_by('level', 'name')
        
        results = []
        for assessment in assessments:
            can_take, reason = AssessmentService.can_take_assessment(child, assessment)
            
            best_attempt = AssessmentAttempt.objects.filter(
                child=child,
                assessment=assessment,
                passed=True
            ).order_by('-percentage').first()
            
            results.append({
                'id': str(assessment.id),
                'name': assessment.name,
                'type': assessment.assessment_type,
                'level': assessment.level,
                'questions_count': assessment.questions_count,
                'time_limit_minutes': assessment.time_limit_minutes,
                'passing_score': assessment.passing_score,
                'can_take': can_take,
                'reason': reason if not can_take else None,
                'best_score': best_attempt.percentage if best_attempt else None,
            })
        
        return results
\`\`\`

---

## 9. Management Commands

### apps/curriculum/management/commands/seed_all.py

\`\`\`python
"""Management command to seed all BhashaMitra data."""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Seed all BhashaMitra data (badges, alphabet, vocabulary)'

    def add_arguments(self, parser):
        parser.add_argument('--badges', action='store_true', help='Seed badges only')
        parser.add_argument('--alphabet', action='store_true', help='Seed alphabet only')
        parser.add_argument('--vocabulary', action='store_true', help='Seed vocabulary only')
        parser.add_argument('--all', action='store_true', help='Seed everything (default)')

    def handle(self, *args, **options):
        from scripts.seed_badges import seed_badges
        from scripts.seed_hindi_alphabet import seed_hindi_alphabet
        from scripts.seed_vocabulary_themes import seed_vocabulary
        
        # Default to seeding everything
        seed_everything = options['all'] or not any([
            options['badges'], options['alphabet'], options['vocabulary']
        ])
        
        if options['badges'] or seed_everything:
            self.stdout.write('Seeding badges...')
            seed_badges()
        
        if options['alphabet'] or seed_everything:
            self.stdout.write('Seeding Hindi alphabet...')
            seed_hindi_alphabet()
        
        if options['vocabulary'] or seed_everything:
            self.stdout.write('Seeding vocabulary themes...')
            seed_vocabulary()
        
        self.stdout.write(self.style.SUCCESS('\n✓ All seeding complete!'))
\`\`\`

### apps/curriculum/management/commands/reset_child_progress.py

\`\`\`python
"""Reset all progress for a child (for testing)."""
from django.core.management.base import BaseCommand, CommandError
from apps.children.models import Child


class Command(BaseCommand):
    help = 'Reset all progress for a child (for testing)'

    def add_arguments(self, parser):
        parser.add_argument('child_id', type=str, help='Child UUID')
        parser.add_argument('--confirm', action='store_true', help='Confirm reset')

    def handle(self, *args, **options):
        try:
            child = Child.objects.get(id=options['child_id'])
        except Child.DoesNotExist:
            raise CommandError(f"Child not found: {options['child_id']}")
        
        if not options['confirm']:
            self.stdout.write(self.style.WARNING(
                f"This will reset ALL progress for {child.name}. Use --confirm to proceed."
            ))
            return
        
        # Reset all progress
        child.progress_records.all().delete()
        child.letter_progress.all().delete()
        child.word_progress.all().delete()
        child.grammar_progress.all().delete()
        child.game_sessions.all().delete()
        child.assessment_attempts.all().delete()
        child.earned_badges.all().delete()
        
        # Reset streak
        if hasattr(child, 'streak'):
            child.streak.current_streak = 0
            child.streak.save()
        
        # Reset points and level
        child.total_points = 0
        child.level = 1
        child.save()
        
        self.stdout.write(self.style.SUCCESS(f"✓ Reset all progress for {child.name}"))
\`\`\`

---

## 10. Summary

### Models Created (22 total)

| Module | Models | Count |
|--------|--------|-------|
| Script/Alphabet | Script, AlphabetCategory, Letter, Matra, LetterProgress | 5 |
| Vocabulary | VocabularyTheme, VocabularyWord, WordProgress | 3 |
| Grammar | GrammarTopic, GrammarRule, GrammarExercise, GrammarProgress | 4 |
| Games | Game, GameSession, GameLeaderboard | 3 |
| Assessment | Assessment, AssessmentQuestion, AssessmentAttempt, Certificate | 4 |
| **Total** | | **19** + 3 from Part 2 = **22** |

### Seed Data Included

- **Badges**: 12 achievement badges (stories, streaks, voice, points)
- **Hindi Alphabet**: 13 vowels, 32 consonants, 12 matras (57 characters)
- **Vocabulary**: 5 themes with 42 words (Family, Colors, Numbers, Animals, Food)

### Key Features

1. **SM-2 Spaced Repetition**: Research-backed algorithm for vocabulary retention
2. **Progress Tracking**: Per-letter, per-word, per-topic granular tracking
3. **Gamification**: Games, leaderboards, achievements
4. **Assessments**: Placement tests, level-up tests, certificates
5. **Multi-Language Ready**: Schema supports Hindi, Tamil, Gujarati, Punjabi, Telugu, Malayalam

### Quick Commands

\`\`\`bash
# Run migrations
python manage.py makemigrations curriculum
python manage.py migrate

# Seed all data
python manage.py seed_all

# Seed specific data
python manage.py seed_all --badges
python manage.py seed_all --alphabet
python manage.py seed_all --vocabulary

# Reset child progress (testing)
python manage.py reset_child_progress <child_uuid> --confirm
\`\`\`

---

## Next: Part 4

Part 4 will cover:
- Complete serializers for all 22 models
- ViewSets and API views
- Additional seed data (Tamil alphabet, more vocabulary)
- Grammar topics and exercises
- Sample games and assessments

---

*End of Part 3*
