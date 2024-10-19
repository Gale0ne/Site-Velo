from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import Reservation, Velo
from reservations.forms import ReservationForm
from django.shortcuts import redirect

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
            return redirect("page_test")
    else:
        form = ReservationForm()

    return render(request, 'reservations/ajout_velo.html', {'form' : form})

def page_test(request):
    reservations = Reservation.objects.all()
    return HttpResponse(f'Hello C moi {reservations[0].eleve} ')
