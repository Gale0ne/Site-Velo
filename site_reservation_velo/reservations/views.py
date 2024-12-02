from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.core.mail import send_mail

from reservations.models import Reservation, User
from reservations.forms import ReservationForm, ReturnVeloForm, LoginForm, SignupForm, IncidentForm

@login_required
def page_reservations(request):
    maintenant = now()
    reservations = Reservation.objects.filter(complete=False).order_by('end_time')
    return render(request, 'reservations/reservations.html', {'reservations' : reservations, 'now' : maintenant})

@login_required
def ajout_velo(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST, user=request.user)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.velo.est_disponible = False
            reservation.code = reservation.changer_code()
            reservation.velo.save()
            reservation.save()
            send_mail(
                subject='Confirmation de votre réservation de vélo',
                message=f"""
Bonjour {request.user.first_name},

Merci d'avoir réservé un vélo. Voici les détails de votre réservation :

- Début de la réservation : {reservation.start_time}
- Fin de la réservation : {reservation.end_time}
- Code de l'antivol : {reservation.code}

Bonne journée !

L'équipe Vélyce
""",
                from_email='gregoire.chappuis777@gmail.com',
                recipient_list=[request.user.email],
                fail_silently=False,
            )
            return redirect("redirect_ajout_reservation", reservation_id=reservation.id)
    else:
        form = ReservationForm(user=request.user)

    return render(request, 'reservations/ajout_velo.html', {'form' : form})

@login_required
def page_test(request):
    reservations = Reservation.objects.all()
    return HttpResponse(f'Hello C moi {reservations[0].eleve} ')

@login_required
def return_velo(request):
    if request.method == 'POST':
        form = ReturnVeloForm(request.POST)
        if form.is_valid():
            velo = form.cleaned_data['velo']
            # Filtrer les réservations actives
            reservations = Reservation.objects.filter(
                velo=velo,
                start_time__lte=now(),
                velo__est_disponible=False,
                eleve=f"{request.user.first_name} {request.user.last_name}",
                complete=False
            )

            if not reservations.exists():
                form.add_error(None, "Aucune réservation active trouvée pour ce vélo. Si tu es sûr de ne pas avoir fait d'erreur, vérifie que tu es bien connecté sur le bon compte.")
                return render(request, 'reservations/return_velo.html', {'form': form})

            reservation = reservations.first()
            reservation.return_velo()
            return redirect('page_reservation')
    else: 
        form = ReturnVeloForm()
    return render(request, 'reservations/return_velo.html', {'form' : form}) 

def login_page(request):
    form = LoginForm()
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=username_or_email)
                username = user.username
            except User.DoesNotExist:
                username = username_or_email
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('page_reservation')
            else:
                message = 'Identifiants incorrects'
    return render(request, 'reservations/login.html', {'form' : form, 'message' : message})

@login_required
def logout_page(request):
    logout(request)
    return redirect("login")

def signup_page(request):
    if not request.user.is_authenticated:
        return redirect('redirect_signup')
    elif request.user.role != 'moderateur':
        return redirect('redirect_signup')
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('page_reservation')
    return render(request, 'reservations/signup.html', {'form' : form})

def redirect_signup(request):
    return render(request, 'reservations/redirect_creation_compte.html')


@login_required
def redirect_ajout_reservation(request, reservation_id):
    from .models import Reservation
    reservation = Reservation.objects.get(id=reservation_id)
    return render(request, 'reservations/redirect_ajout_reservation.html', {
        'user': request.user,
        'reservation': reservation
    })

@login_required
def signaler_incident(request):
    if request.method == 'POST':
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user = request.user
            incident.save()
            return redirect('page_reservation') 
    else:
        form = IncidentForm()
    return render(request, 'reservations/signal_incident.html', {'form': form})