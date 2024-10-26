from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reservations.models import Reservation, Velo
from reservations.forms import ReservationForm, ReturnVeloForm

def page_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservations.html', {'reservations' : reservations})

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

def page_test(request):
    reservations = Reservation.objects.all()
    return HttpResponse(f'Hello C moi {reservations[0].eleve} ')

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
