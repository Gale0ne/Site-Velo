# Generated by Django 5.1.2 on 2024-11-24 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='velo',
            name='code',
        ),
        migrations.AddField(
            model_name='reservation',
            name='code',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]