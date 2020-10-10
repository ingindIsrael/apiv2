# Generated by Django 3.1.2 on 2020-10-10 02:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0011_auto_20201006_0058'),
        ('events', '0004_auto_20200806_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eventbrite_id', models.CharField(blank=True, max_length=30)),
                ('eventbrite_key', models.CharField(blank=True, default=None, max_length=255, null=True)),
                ('name', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('academy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admissions.academy')),
            ],
        ),
        migrations.AddField(
            model_name='venue',
            name='organization',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='events.organizacion'),
        ),
    ]
