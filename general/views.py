from django.shortcuts import render
from utilisateur.models import Utilisateur
from general.models import Personne, ArticleForm, Article
from django.contrib.auth import login
from django.shortcuts import redirect
# Create your views here.


def accueil(request):
   # user = Utilisateur.objects.create_user('bil1', 'bil1@gmail.com', 'bil123456', first_name='Bilali1', last_name='Diallo')
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
    utilisateur = Utilisateur.objects.create_user(user_name, email, password, first_name= first_name, last_name= first_name)
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











        
"""
def addarticle(request):
    form = ArticleForm()
    print("\n\n\n\n\n +++++++++++++++++++++++++++++++++++++++++++++++")
    print(form)
    print("\n\n\n\n\n")
    render(request, "general/newarticle.html", context={'form': form})
    
"""