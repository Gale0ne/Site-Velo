from django import forms
from reservations.models import Reservation, Velo, User, Incident
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.core.exceptions import ValidationError
from datetime import timedelta

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['eleve', 'velo', 'start_time', 'end_time']
        labels = {
            'eleve': "Élève",
            'velo': 'Vélo',
            'start_time': 'Heure de départ de la réservation',
            'end_time': 'Heure de fin de la réservation'
        }
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetime-field', 
                'placeholder': 'Début de la réservation',
                'type': 'datetime-local',
            }),
            'end_time': forms.DateTimeInput(attrs={
                'class': 'form-control datetime-field',         
                'placeholder': 'Fin de la réservation',
                'type': 'datetime-local'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Limiter les choix d'élèves pour les modérateurs
        if self.user and self.user.is_staff:
            self.fields['eleve'].queryset = User.objects.all()
        else:
            self.fields['eleve'].queryset = User.objects.filter(id=self.user.id)

        # Initialisation automatique pour l'utilisateur connecté
        if not self.user.is_staff:
            self.fields['eleve'].initial = self.user
            self.fields['eleve'].widget.attrs['disabled'] = False  # Désactiver le champ pour un utilisateur non modérateur

        self.fields['start_time'].initial = now()

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        velo = cleaned_data.get('velo')

        # Vérifier les chevauchements
        if velo and start_time and end_time:
            overlapping_reservations = Reservation.objects.filter(
                velo=velo,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if overlapping_reservations.exists():
                raise ValidationError("Ce vélo est déjà réservé pour cette plage horaire.")

        # Vérifie que start_time est avant end_time
        if start_time and end_time and start_time >= end_time:
            raise ValidationError("L'heure de début doit être avant l'heure de fin.")

        # Vérifie que la réservation n'est pas dans le passé
        if start_time and start_time < now():
            raise ValidationError("La réservation ne peut pas commencer dans le passé.")

        # Vérifie que l'intervalle entre start_time et end_time ne dépasse pas 8 heures
        if start_time and end_time:
            max_duration = timedelta(hours=8)
            if end_time - start_time > max_duration:
                raise ValidationError("La durée de la réservation ne peut pas dépasser 8 heures.")

        # Désactiver l'utilisateur si le champ est désactivé
        if not self.user.is_staff:
            cleaned_data['eleve'] = self.user

        return cleaned_data

class ReturnVeloForm(forms.Form):
    velo = forms.ModelChoiceField(
        queryset=Velo.objects.filter(est_disponible=False),  
        label="Sélectionnez un vélo à retourner"
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Mot de passe")

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'classe']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse e-mail est déjà associée à un compte.")
        return email

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['velo', 'description', 'photo']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez le problème rencontré avec le vélo',
                'rows': 5
            }),
            'velo': forms.Select(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
