from django.db import models

class Reservation(models.Model):
    VELO_CHOICES = [
        ('Velo1', 'Velo 1'),
        ('Velo2', 'Velo 2'),
    ]
    eleve = models.fields.CharField(max_length=100)
    heure_reservation = models.DateTimeField()
    velo = models.CharField(max_length=5, choices=VELO_CHOICES, default='Velo1')