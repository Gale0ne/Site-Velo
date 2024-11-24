from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from random import randint

class Velo(models.Model):
    VELO_CHOICES = [
        ('Velo1', 'Velo 1'),
        ('Velo2', 'Velo 2'),
    ]
    velo = models.CharField(max_length=5, choices=VELO_CHOICES, default='Velo1')
    est_disponible = models.BooleanField(default=True)
    code = models.IntegerField(null=True, blank=True)

    def changer_code(self):
        return randint(1000, 9999)

class Reservation(models.Model):
    velo = models.ForeignKey(Velo, on_delete=models.CASCADE)
    eleve = models.fields.CharField(max_length=100)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)

    def return_velo(self):
        self.end_time = timezone.now()
        self.velo.est_disponible = True
        self.velo.code = self.velo.changer_code()
        self.save()
        self.velo.save()

class User(AbstractUser):
    CLASSE_CHOICES = [
        ("TG1", "TG1"), 
        ("TG2", "TG2"), 
        ("TG3", "TG3"), 
        ("TG4", "TG4"), 
    ]
    classe = models.CharField(max_length=5, choices=CLASSE_CHOICES, default="TG1")