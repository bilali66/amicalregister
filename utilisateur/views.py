from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from general.models import Personne
from general.views import accueil
# Create your views here.



def connexionformul(request):
        return render(request, 'general/connexion.html', {'badcredential':False})


def deconnexion(request):
    logout(request)
    return redirect("accueil")


def connexion(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        #personne = Personne.objects.get(user=user)
        login(request, user)
        return redirect("panier")
    return render(request, 'general/connexion.html', {'badcredential':True})
