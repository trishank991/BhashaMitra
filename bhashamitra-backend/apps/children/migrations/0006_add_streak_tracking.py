# Generated manually for streak tracking fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('children', '0005_add_fiji_hindi_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='child',
            name='current_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='child',
            name='longest_streak',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='child',
            name='last_activity_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
