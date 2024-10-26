from django.db import models
from django.utils import timezone

class Velo(models.Model):
    VELO_CHOICES = [
        ('Velo1', 'Velo 1'),
        ('Velo2', 'Velo 2'),
    ]
    velo = models.CharField(max_length=5, choices=VELO_CHOICES, default='Velo1')
    est_disponible = models.BooleanField(default=True)

class Reservation(models.Model):
    velo = models.ForeignKey(Velo, on_delete=models.CASCADE)
    eleve = models.fields.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def return_velo(self):
        self.end_time = timezone.now()
        self.velo.est_disponible = True
        self.save()
        self.velo.save()
