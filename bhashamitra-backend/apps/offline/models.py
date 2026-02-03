"""Offline mode models for PWA support."""
from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel


class OfflinePackage(TimeStampedModel):
    """Pre-packaged content for offline use."""

    class PackageType(models.TextChoices):
        FREE_TIER = 'FREE_TIER', 'Free Tier Package'
        LANGUAGE_PACK = 'LANGUAGE_PACK', 'Language Pack'
        CURRICULUM_MODULE = 'CURRICULUM_MODULE', 'Curriculum Module'
        FESTIVAL_PACK = 'FESTIVAL_PACK', 'Festival Pack'

    name = models.CharField(max_length=200)
    package_type = models.CharField(
        max_length=30,
        choices=PackageType.choices,
        default=PackageType.FREE_TIER
    )
    language = models.CharField(max_length=20)
    version = models.CharField(max_length=20, default='1.0.0')
    size_mb = models.DecimalField(max_digits=8, decimal_places=2)
    content_manifest = models.JSONField(
        default=dict,
        help_text='JSON manifest of included stories, audio, images'
    )
    is_active = models.BooleanField(default=True)
    min_app_version = models.CharField(max_length=20, default='1.0.0')

    class Meta:
        db_table = 'offline_packages'
        indexes = [
            models.Index(fields=['language', 'package_type']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.language})"


class ChildOfflineContent(TimeStampedModel):
    """Tracks offline content downloaded per child."""

    class SyncStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending Sync'
        SYNCED = 'SYNCED', 'Synced'
        FAILED = 'FAILED', 'Sync Failed'

    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='offline_content'
    )
    package = models.ForeignKey(
        OfflinePackage,
        on_delete=models.CASCADE,
        related_name='downloads'
    )
    downloaded_at = models.DateTimeField(auto_now_add=True)
    last_sync_at = models.DateTimeField(null=True, blank=True)
    sync_status = models.CharField(
        max_length=20,
        choices=SyncStatus.choices,
        default=SyncStatus.PENDING
    )
    offline_progress = models.JSONField(
        default=dict,
        help_text='Progress made while offline'
    )
    storage_used_mb = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'child_offline_content'
        unique_together = ['child', 'package']
        indexes = [
            models.Index(fields=['child', 'sync_status']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.package.name}"
