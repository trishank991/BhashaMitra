"""Child profile models."""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel, SoftDeleteModel, SoftDeleteManager


class Child(TimeStampedModel, SoftDeleteModel):
    """Child profile linked to a parent user."""

    class Language(models.TextChoices):
        FIJI_HINDI = 'FIJI_HINDI', 'Fiji Hindi'
        GUJARATI = 'GUJARATI', 'Gujarati'
        HINDI = 'HINDI', 'Hindi'
        MALAYALAM = 'MALAYALAM', 'Malayalam'
        PUNJABI = 'PUNJABI', 'Punjabi'
        TAMIL = 'TAMIL', 'Tamil'
        TELUGU = 'TELUGU', 'Telugu'

    class PeppiAddressing(models.TextChoices):
        BY_NAME = 'BY_NAME', 'By Name'
        CULTURAL = 'CULTURAL', 'Cultural (Bhaiya/Didi)'

    class PeppiGender(models.TextChoices):
        MALE = 'MALE', 'Male (Peppi Bhaiya)'
        FEMALE = 'FEMALE', 'Female (Peppi Didi)'

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='children'
    )
    name = models.CharField(max_length=100)
    avatar = models.CharField(max_length=50, default='default')
    date_of_birth = models.DateField()
    language = models.CharField(
        max_length=20,
        choices=Language.choices,
        default=Language.HINDI
    )
    level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    total_points = models.IntegerField(default=0)

    # Peppi preferences
    peppi_addressing = models.CharField(
        max_length=20,
        choices=PeppiAddressing.choices,
        default=PeppiAddressing.BY_NAME,
        help_text='How Peppi addresses the child'
    )
    peppi_gender = models.CharField(
        max_length=10,
        choices=PeppiGender.choices,
        default=PeppiGender.FEMALE,
        help_text='Peppi voice gender preference'
    )

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        db_table = 'children'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['language', 'level']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.email})"

    @property
    def age(self):
        from apps.core.utils import calculate_age
        return calculate_age(self.date_of_birth)
