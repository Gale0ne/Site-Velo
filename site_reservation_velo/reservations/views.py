from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reservations.models import Reservation, Velo
from reservations.forms import ReservationForm, ReturnVeloForm, LoginForm, SignupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

@login_required
def page_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservations.html', {'reservations' : reservations})

@login_required
def ajout_velo(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.velo.est_disponible = False
            reservation.velo.save()
            reservation.save()
            return redirect("page_reservation")
    else:
        form = ReservationForm()

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
            reservation = get_object_or_404(Reservation, velo=velo, end_time__isnull=True)
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
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
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
    form = SignupForm()
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('page_reservation')
    return render(request, 'reservations/signup.html', {'form' : form})