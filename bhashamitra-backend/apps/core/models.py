"""Base models for the application."""
import uuid
from django.db import models


class Tenant(models.Model):
    """Multi-tenant foundation model.

    Represents an organization/school/institution that uses PeppiAcademy.
    For now, all users belong to the default 'PeppiAcademy' tenant.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, help_text='Organization name')
    slug = models.SlugField(max_length=100, unique=True, help_text='URL-safe identifier')
    domain = models.CharField(
        max_length=255, blank=True, null=True, unique=True,
        help_text='Custom domain for this tenant (e.g., school.peppiacademy.com)'
    )
    logo_url = models.URLField(blank=True, null=True, help_text='Tenant logo URL')
    theme_config = models.JSONField(
        default=dict, blank=True,
        help_text='Custom theme configuration (colors, branding)'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class TimeStampedModel(models.Model):
    """Abstract model with created/updated timestamps."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteManager(models.Manager):
    """Manager that excludes soft-deleted records by default."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """Abstract model with soft delete capability."""
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()  # Include deleted records

    class Meta:
        abstract = True

    def soft_delete(self):
        """Mark record as deleted."""
        from django.utils import timezone
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self):
        return self.deleted_at is not None
