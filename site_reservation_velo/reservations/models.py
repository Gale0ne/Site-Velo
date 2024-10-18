from django.db import models

class Reservation(models.Model):
    eleve = models.fields.CharField(max_length=100)
    heure_reservation = models.DateField()