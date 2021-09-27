# Generated by Django 3.0.8 on 2020-07-17 20:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('freelance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='author',
            field=models.ForeignKey(default=None,
                                    null=True,
                                    on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='duration_in_minutes',
            field=models.FloatField(default=0),
        ),
    ]
