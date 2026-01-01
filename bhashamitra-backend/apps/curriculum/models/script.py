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
    example_image = models.URLField(blank=True, null=True)
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
