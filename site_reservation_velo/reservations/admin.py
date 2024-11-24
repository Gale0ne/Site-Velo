from django.contrib import admin
from .models import Reservation, Velo, User

admin.site.register(Reservation)
admin.site.register(Velo)
admin.site.register(User)