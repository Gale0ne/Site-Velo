# Generated by Django 5.1.2 on 2024-10-18 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_alter_reservation_heure_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='velo',
            field=models.CharField(choices=[('Velo1', 'Velo 1'), ('Velo2', 'Velo 2')], default='Velo1', max_length=5),
        ),
    ]