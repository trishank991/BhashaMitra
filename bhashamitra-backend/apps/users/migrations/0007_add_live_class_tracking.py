# Generated manually for live class tracking fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_add_onboarding_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='live_classes_used_this_month',
            field=models.IntegerField(default=0, help_text='Number of live classes used in the current month'),
        ),
        migrations.AddField(
            model_name='user',
            name='live_classes_month',
            field=models.DateField(blank=True, null=True, help_text='The month for which live_classes_used_this_month is tracked'),
        ),
    ]
