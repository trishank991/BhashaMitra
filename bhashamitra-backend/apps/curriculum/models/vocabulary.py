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

    def __str__(self):
        return f"{self.name} ({self.language})"

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

    def __str__(self):
        return f"{self.word} - {self.translation}"


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
