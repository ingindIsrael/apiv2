# Generated by Django 3.2.9 on 2021-12-20 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment', '0003_alter_assessment_original'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assessment',
            name='original',
            field=models.ForeignKey(
                blank=True,
                default=None,
                help_text=
                'The original translation (will only be set if the quiz is a translation of another one)',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='translations',
                to='assessment.assessment'),
        ),
    ]
