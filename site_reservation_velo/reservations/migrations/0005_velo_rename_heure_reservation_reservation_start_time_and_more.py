# Generated by Django 5.1.2 on 2024-10-19 10:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0004_reservation_velo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Velo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('velo', models.CharField(choices=[('Velo1', 'Velo 1'), ('Velo2', 'Velo 2')], default='Velo1', max_length=5)),
                ('est_disponible', models.BooleanField(default=True)),
            ],
        ),
        migrations.RenameField(
            model_name='reservation',
            old_name='heure_reservation',
            new_name='start_time',
        ),
        migrations.AddField(
            model_name='reservation',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='velo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservations.velo'),
        ),
    ]
