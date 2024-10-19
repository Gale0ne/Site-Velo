from django import forms
from reservations.models import Reservation, Velo

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['velo', 'eleve']
        
    def clean_velo(self):
        velo = self.cleaned_data.get('velo')
        if not velo.est_disponible:
            raise forms.ValidationError("Ce vélo est déjà reservé.")
        return velo
