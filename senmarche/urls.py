"""
URL configuration for senmarche project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from general import views
from utilisateur.views import connexion, connexionformul, deconnexion
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls, name='admin'), 
    path("panier/", views.panier, name='panier'),
    path("panier/confirmPanier", views.confirmPanier, name='confirmPanier'),
    path("commander/<str:id>/", views.commander, name='commander'),
    path("accueil", views.accueil, name='accueil'),
    path("", views.inscription, name='inscription'),
    path("newPersonne", views.newPersonne, name='newPersonne'),
    path("addarticle", views.addarticle, name='addarticle'), 
    path("newarcticle", views.newarcticle, name='newarcticle'),
    path("connexionformul/", connexionformul , name='connexionformul'),
    path("connexionformul/connexion", connexion , name='connexion'),
    path("deconnexion", deconnexion , name='deconnexion'),
    path('download/etudiants/excel/', views.download_etudiants_excel, name='download_etudiants_excel'),
    path('download/etudiants/pdf/', views.download_etudiants_pdf, name='download_etudiants_pdf'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
