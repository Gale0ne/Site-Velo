from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from random import randint

class User(AbstractUser):
    CLASSE_CHOICES = [
        ("TG1", "TG1"), 
        ("TG2", "TG2"), 
        ("TG3", "TG3"), 
        ("TG4", "TG4"), 
    ]

    ROLE_CHOICES = [
        ("eleve", "Élève"), 
        ("moderateur", "Modérateur"), 
    ]
    classe = models.CharField(max_length=5, choices=CLASSE_CHOICES, default="TG1")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='eleve')

class Incident(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    velo = models.ForeignKey('Velo', on_delete=models.CASCADE, verbose_name="Vélo")
    description = models.TextField(verbose_name="Description de l'incident")
    photo = models.ImageField(upload_to='incident_photos/', blank=True, null=True, verbose_name="Photo (facultative)")
    reported_at = models.DateTimeField(auto_now_add=True, verbose_name="Date de signalement")

    def __str__(self):
        return f"Incident signalé par {self.user.username} pour le {self.velo}"


class Velo(models.Model):
    VELO_CHOICES = [
        ('Velo 1', 'Velo 1'),
        ('Velo 2', 'Velo 2'),
    ]
    velo = models.CharField(max_length=6, choices=VELO_CHOICES, default='Velo1')
    est_disponible = models.BooleanField(default=True)
    
    def __str__(self):
        return self.velo

class Reservation(models.Model):
    velo = models.ForeignKey(Velo, on_delete=models.CASCADE)
    eleve = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    code = models.IntegerField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def return_velo(self):
        self.end_time = timezone.now()
        self.velo.est_disponible = True
        self.complete = True
        self.save()
        self.velo.save()

    def changer_code(self):
        return randint(1000, 9999)
    
    def __str__(self):
        return f'{self.complete} {self.eleve} de {self.start_time} à {self.end_time}'

