# Generated manually on 2025-12-27
# Migration for adding onboarding fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_add_email_verification'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_onboarded',
            field=models.BooleanField(
                default=False,
                help_text='Whether the user has completed the onboarding process'
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='onboarding_completed_at',
            field=models.DateTimeField(
                blank=True,
                null=True,
                help_text='When the user completed onboarding'
            ),
        ),
    ]
