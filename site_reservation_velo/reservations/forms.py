from django import forms
from reservations.models import Reservation, Velo, User

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['velo', 'eleve']
        
    def clean_velo(self):
        velo = self.cleaned_data.get('velo')
        if not velo.est_disponible:
            raise forms.ValidationError("Ce vélo est déjà reservé.")
        return velo

class ReturnVeloForm(forms.Form):
    velo = forms.ModelChoiceField(
        queryset=Velo.objects.filter(est_disponible=False),  
        label="Sélectionnez un vélo à retourner"
    )

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Mot de passe")