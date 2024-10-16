from django.shortcuts import render
from django.http import HttpResponse

def page_reservations(request):
    return render(request, 'reservations/reservations.html')
