# Generated manually for acoustic scoring enhancement

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('speech', '0003_peppimimicchallenge_peppimimicattempt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='peppimimicattempt',
            name='audio_energy_score',
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100)
                ],
                help_text='RMS energy analysis score 0-100'
            ),
        ),
        migrations.AddField(
            model_name='peppimimicattempt',
            name='duration_match_score',
            field=models.FloatField(
                default=0,
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100)
                ],
                help_text='Duration similarity to reference 0-100'
            ),
        ),
        migrations.AddField(
            model_name='peppimimicattempt',
            name='scoring_version',
            field=models.PositiveSmallIntegerField(
                default=2,
                help_text='Scoring algorithm version (1=STT+text, 2=hybrid with acoustic)'
            ),
        ),
    ]
