"""
URL configuration for site_reservation_velo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservations import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('reservations/', views.page_reservations, name='page_reservation'),
    path('ajout_reservation/', views.ajout_velo, name='ajout_reservation'),
    path('page_test/', views.page_test, name='page_test'),
    path('rendre_velo/', views.return_velo, name='return_bike'),
    path('', views.login_page, name="login"),
    path('logout', views.logout_page, name='logout'),
    path('signup/', views.signup_page, name='signup'),
    path('redirection_creation_compte/', views.redirect_signup, name='redirect_signup'),
    path('redirection_ajout_reservation/<int:reservation_id>/', views.redirect_ajout_reservation, name='redirect_ajout_reservation'),
    path('signaler_incident/', views.signaler_incident, name='signaler_incident'),
]


if settings.DEBUG: # Servir les fichiers média uniquement en mode développement
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)