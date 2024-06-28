from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from general.models import Personne
# Create your views here.



def connexionformul(request):
        return render(request, 'general/connexion.html')


def deconnexion(request):
    logout(request)
    return render(request, 'general/accueil.html')


def connexion(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        personne = Personne.objects.get(user=user)
        login(request, user)
        return render(request, 'general/accueil.html', {'user':personne})
    return render(request, 'general/accueil.html')
