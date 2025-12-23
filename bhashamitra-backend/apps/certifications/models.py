"""Certification and achievement models."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
import secrets


def generate_certificate_id():
    return f"BM-{secrets.token_hex(8).upper()}"


class CertificateTemplate(TimeStampedModel):
    """Templates for printable certificates."""

    class CertificateType(models.TextChoices):
        LEVEL_COMPLETION = 'LEVEL_COMPLETION', 'Level Completion'
        LANGUAGE_PROFICIENCY = 'LANGUAGE_PROFICIENCY', 'Language Proficiency'
        CULTURAL_KNOWLEDGE = 'CULTURAL_KNOWLEDGE', 'Cultural Knowledge'
        SPECIAL_ACHIEVEMENT = 'SPECIAL_ACHIEVEMENT', 'Special Achievement'
        ANNUAL_PROGRESS = 'ANNUAL_PROGRESS', 'Annual Progress'

    name = models.CharField(max_length=200)
    certificate_type = models.CharField(max_length=30, choices=CertificateType.choices)
    template_html = models.TextField()
    template_css = models.TextField(blank=True)
    background_image = models.URLField(blank=True)
    language = models.CharField(max_length=20, blank=True, help_text='Blank for all languages')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'certificate_templates'

    def __str__(self):
        return f"{self.name} ({self.certificate_type})"


class PrintableCertificate(TimeStampedModel):
    """Printable certificates for children (extends curriculum Certificate functionality)."""

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='printable_certificates'
    )
    template = models.ForeignKey(
        CertificateTemplate,
        on_delete=models.PROTECT,
        related_name='issued_certificates'
    )
    certificate_id = models.CharField(
        max_length=30,
        unique=True,
        default=generate_certificate_id
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    issued_date = models.DateField(auto_now_add=True)
    achievement_data = models.JSONField(
        default=dict,
        help_text='Data used to populate certificate (level, scores, etc.)'
    )
    pdf_url = models.URLField(blank=True)
    is_shared = models.BooleanField(default=False)
    share_url = models.URLField(blank=True)

    class Meta:
        db_table = 'printable_certificates'
        indexes = [
            models.Index(fields=['child', 'issued_date']),
            models.Index(fields=['certificate_id']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.title}"


class AnnualProgressReport(TimeStampedModel):
    """Comprehensive annual progress reports."""

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='annual_reports'
    )
    year = models.IntegerField()
    report_data = models.JSONField(
        default=dict,
        help_text='Comprehensive yearly statistics'
    )
    starting_level = models.IntegerField(default=1)
    ending_level = models.IntegerField(default=1)
    total_stories_read = models.IntegerField(default=0)
    total_points_earned = models.IntegerField(default=0)
    total_time_minutes = models.IntegerField(default=0)
    words_learned = models.IntegerField(default=0)
    letters_mastered = models.IntegerField(default=0)
    achievements_earned = models.JSONField(default=list)
    monthly_breakdown = models.JSONField(default=dict)
    pdf_url = models.URLField(blank=True)
    generated_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'annual_progress_reports'
        unique_together = ['child', 'year']

    def __str__(self):
        return f"{self.child.name} - {self.year} Report"
