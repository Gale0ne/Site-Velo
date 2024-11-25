from django import forms
from reservations.models import Reservation, Velo
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['eleve', 'velo']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        self.fields['eleve'].initial = f"{self.user.first_name} {self.user.last_name}"
        # self.fields['eleve'].widget.attrs['disabled'] = True
        
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

class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'classe']