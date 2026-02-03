"""Progress tracking models for curriculum hierarchy."""
import uuid
from django.db import models
from django.utils import timezone
from apps.core.models import TimeStampedModel
from .level import CurriculumLevel, CurriculumModule, Lesson


class LevelProgress(TimeStampedModel):
    """Tracks a child's progress through a curriculum level."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='level_progress'
    )
    level = models.ForeignKey(
        CurriculumLevel,
        on_delete=models.CASCADE,
        related_name='child_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    modules_completed = models.PositiveSmallIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'level_progress'
        unique_together = ['child', 'level']
        indexes = [
            models.Index(fields=['child', 'is_complete']),
            models.Index(fields=['level']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.level.code}"

    def mark_complete(self):
        """Mark level as complete."""
        if not self.is_complete:
            self.is_complete = True
            self.completed_at = timezone.now()
            self.save(update_fields=['is_complete', 'completed_at', 'updated_at'])


class ModuleProgress(TimeStampedModel):
    """Tracks a child's progress through a curriculum module."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='module_progress'
    )
    module = models.ForeignKey(
        CurriculumModule,
        on_delete=models.CASCADE,
        related_name='child_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    lessons_completed = models.PositiveSmallIntegerField(default=0)
    total_points = models.PositiveIntegerField(default=0)
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'module_progress'
        unique_together = ['child', 'module']
        indexes = [
            models.Index(fields=['child', 'is_complete']),
            models.Index(fields=['module']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.module.code}"

    def mark_complete(self):
        """Mark module as complete and update level progress."""
        if not self.is_complete:
            self.is_complete = True
            self.completed_at = timezone.now()
            self.save(update_fields=['is_complete', 'completed_at', 'updated_at'])

            # Update level progress
            level_progress, _ = LevelProgress.objects.get_or_create(
                child=self.child,
                level=self.module.level
            )
            level_progress.modules_completed += 1
            level_progress.save(update_fields=['modules_completed', 'updated_at'])


class LessonProgress(TimeStampedModel):
    """Tracks a child's progress through a lesson."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    child = models.ForeignKey(
        'children.Child',
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='child_progress'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.PositiveSmallIntegerField(default=0, help_text='Latest score percentage')
    attempts = models.PositiveSmallIntegerField(default=0, help_text='Number of attempts')
    best_score = models.PositiveSmallIntegerField(default=0, help_text='Best score achieved')
    is_complete = models.BooleanField(default=False)

    class Meta:
        db_table = 'lesson_progress'
        unique_together = ['child', 'lesson']
        indexes = [
            models.Index(fields=['child', 'is_complete']),
            models.Index(fields=['lesson']),
        ]

    def __str__(self):
        return f"{self.child.name} - {self.lesson.code}"

    def update_progress(self, score):
        """Update lesson progress with new score."""
        self.attempts += 1
        self.score = score
        self.best_score = max(self.best_score, score)

        # Check if mastered
        if score >= self.lesson.mastery_threshold and not self.is_complete:
            self.is_complete = True
            self.completed_at = timezone.now()

            # Update module progress
            module_progress, _ = ModuleProgress.objects.get_or_create(
                child=self.child,
                module=self.lesson.module
            )
            module_progress.lessons_completed += 1
            module_progress.total_points += self.lesson.points_available
            module_progress.save(update_fields=['lessons_completed', 'total_points', 'updated_at'])

        self.save()
