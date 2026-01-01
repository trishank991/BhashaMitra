"""Verified content models for quality assurance."""
from django.db import models
from django.contrib.auth import get_user_model
from apps.core.models import TimeStampedModel

User = get_user_model()


class VerifiedLetter(TimeStampedModel):
    """Verified alphabet letter with quality checks."""

    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'
        NEEDS_REVISION = 'NEEDS_REVISION', 'Needs Revision'

    language = models.CharField(max_length=20)
    character = models.CharField(max_length=10)  # The letter in native script
    romanization = models.CharField(max_length=50)
    pronunciation_guide = models.CharField(max_length=200)
    example_word = models.CharField(max_length=100, blank=True)
    example_word_meaning = models.CharField(max_length=200, blank=True)
    example_image = models.URLField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)

    # Verification
    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default='PENDING')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_letters')
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    # Quality scores (1-5)
    pronunciation_accuracy = models.IntegerField(default=0)
    example_relevance = models.IntegerField(default=0)

    class Meta:
        db_table = 'verified_letters'
        unique_together = ['language', 'character']
        ordering = ['language', 'character']

    def __str__(self):
        return f"{self.character} ({self.romanization}) - {self.language} [{self.status}]"


class VerifiedWord(TimeStampedModel):
    """Verified vocabulary word with quality checks."""

    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Review'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'
        NEEDS_REVISION = 'NEEDS_REVISION', 'Needs Revision'

    language = models.CharField(max_length=20)
    word = models.CharField(max_length=200)
    romanization = models.CharField(max_length=200)
    translation = models.CharField(max_length=200)
    part_of_speech = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, blank=True)
    example_sentence = models.TextField(blank=True)
    example_sentence_translation = models.TextField(blank=True)
    audio_url = models.URLField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    # Verification
    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default='PENDING')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_words')
    verified_at = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)

    # Quality scores (1-5)
    translation_accuracy = models.IntegerField(default=0)
    cultural_appropriateness = models.IntegerField(default=0)
    age_appropriateness = models.IntegerField(default=0)

    class Meta:
        db_table = 'verified_words'
        unique_together = ['language', 'word']
        ordering = ['language', 'word']

    def __str__(self):
        return f"{self.word} ({self.romanization}) - {self.translation} [{self.status}]"
