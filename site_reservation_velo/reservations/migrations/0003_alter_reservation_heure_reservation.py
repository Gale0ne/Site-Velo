# Generated by Django 5.1.2 on 2024-10-18 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0002_rename_reservations_reservation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='heure_reservation',
            field=models.DateTimeField(),
        ),
    ]