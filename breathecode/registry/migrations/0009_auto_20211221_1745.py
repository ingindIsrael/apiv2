# Generated by Django 3.2.9 on 2021-12-21 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registry', '0008_auto_20211220_1947'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='owner',
            field=models.ForeignKey(blank=True,
                                    default=None,
                                    help_text='The owner has the github premissions to update the lesson',
                                    null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    related_name='owned_lessons',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='asset',
            name='asset_type',
            field=models.CharField(choices=[('PROJECT', 'Project'), ('EXERCISE', 'Exercise'),
                                            ('QUIZ', 'Quiz'), ('LESSON', 'Lesson'), ('VIDEO', 'Video')],
                                   max_length=20),
        ),
        migrations.AlterField(
            model_name='asset',
            name='author',
            field=models.ForeignKey(blank=True,
                                    default=None,
                                    help_text='Who wrote the lesson, not necessarily the owner',
                                    null=True,
                                    on_delete=django.db.models.deletion.SET_NULL,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]
