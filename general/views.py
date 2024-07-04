from django.shortcuts import render
from utilisateur.models import Utilisateur
from general.models import CommandeForm,CommandeFormSet,  Personne, ArticleForm, Article, Commande
from django.contrib.auth import login
from django.shortcuts import redirect
import datetime
from django.core.mail import BadHeaderError, send_mail
# Create your views here.


def accueil(request):
    user = Utilisateur.objects.get(username='bil')
    if user is not None:
        user.is_superuser = True
        user.is_staff = True
        user.save()
    else:
        user = Utilisateur.objects.create_user('bil', 'bil1@gmail.com', 'bil123456', first_name='Bilali1', last_name='Diallo')
        user.is_superuser = True
        user.is_staff = True
        user.save()
        personne = Personne.objects.create(user=user, phone= 'phone', adresse= 'adresse')
    articles = Article.objects.all()
    print("\n\n\n ", len(articles))
    return render(request , 'general/accueil.html',{"articles":articles} )


def inscription(request):
    return render(request , 'general/inscription.html', )

def newPersonne(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    phone = request.POST['phone']
    user_name = request.POST['user_name']
    password = request.POST['password']
    adresse = request.POST['adresse']
    utilisateur = Utilisateur.objects.create_user(user_name, email, password, first_name= first_name, last_name= last_name)
    personne = Personne.objects.create(user=utilisateur, phone= phone, adresse= adresse)
    login(request, utilisateur)
    return redirect("accueil")

def addarticle(request):
    form = ArticleForm()
       # user = Utilisateur.objects.create_user('bil1', 'bil1@gmail.com', 'bil123456', first_name='Bilali1', last_name='Diallo')
    return render(request , 'general/newarticle.html', {"form": form})

    """
    
    
    name = request.POST['name']
    prix = request.POST['prix']
    image = request.POST['image']
    stock = request.POST['stock']
    description = request.POST['description']
    """

def newarcticle(request):
    aform = ArticleForm(request.POST, request.FILES)
    if aform.is_valid():
        article = aform.instance
        user = request.user 
        personne = Personne.objects.get(user = user)
        article.vendeur = personne
        article.save()
    return redirect("accueil")


def panier(request):
    personne = Personne.objects.get(user = request.user)
    #formset = CartItemFormSet(instance=personne)
    commandes =  Commande.objects.filter(acheteur= personne, statut= False)
    forms = CommandeFormSet(queryset=commandes)
    return render(request , 'general/panier.html', {'forms': forms})

def confirmPanier(request):
    personne = Personne.objects.get(user = request.user)
    if request.method == 'POST':
        formset = CommandeFormSet(request.POST, queryset=Commande.objects.filter(acheteur= personne))
        if formset.is_valid():
            formset.save()
            prix = 0
            
            for commande in Commande.objects.filter(acheteur= personne, statut = False):
                    commande.statut = True
                    commande.save()
                    prix += commande.article.prix*commande.quantite
            send_email(personne, prix)
            
        else:
            # Affichez les erreurs dans la console pour déboguer
            print(formset.errors)
            
        
    return redirect('panier') 



def commander(request, id):
    user = request.user 
    personne = Personne.objects.get(user = user)
    article  = Article.objects.get(id = id)
    commande =  Commande.objects.get_or_create(article=article, acheteur= personne, date= datetime.datetime.now())
    return render(request , 'general/inscription.html', )








        
"""
def addarticle(request):
    form = ArticleForm()
    print("\n\n\n\n\n +++++++++++++++++++++++++++++++++++++++++++++++")
    print(form)
    print("\n\n\n\n\n")
    render(request, "general/newarticle.html", context={'form': form})
    
"""



def send_email(personne, prix):
    subject = "Senmarche "
    message = f"Bonjour {personne.user.first_name} {personne.user.last_name} \n \nVous venez d'effectuer une commande de {prix} FCFA à SenMarché.\n\nVotre commande vous sera livrée dans les plus brefs délaies.\n\nMerci d'avoir choisi SenMarché."
    from_email = "senemarche206@gmail.com"
    try:
        send_mail(subject, message, from_email, [personne.user.email])
    except BadHeaderError:
        return False
    return True
   