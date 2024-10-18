from django.shortcuts import render
from django.http import HttpResponse
from reservations.models import Reservation

def page_reservations(request):
    reservations = Reservation.objects.all()
    return render(request, 'reservations/reservations.html', {'reservations' : reservations})

def ajout_velo(request):
    return render(request, 'reservations/ajout_velo.html')

def page_test(request):
    reservations = Reservation.objects.all()
    return HttpResponse(f'Hello C moi {reservations[0].eleve} ')