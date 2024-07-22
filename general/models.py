from django.db import models
from django.conf import settings
from django.forms import  ModelForm, inlineformset_factory, modelformset_factory
# Create your models here.

class Personne(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone = models.CharField(max_length=70)
    adresse = models.CharField(max_length=100)
    #photo = models.ImageField(upload_to= 'UsersImage/')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}: {self.phone} {self.adresse}"
    
    


class Article(models.Model):
    vendeur = models.ForeignKey(Personne, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    prix = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='articleImages/')
    description = models.TextField()
    stock = models.IntegerField(default = 1)
    
    
    def __str__(self):
        return f"{self.name} vendeur: {self.vendeur.phone}"
    
    
    

class Commande(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    acheteur = models.ForeignKey(Personne, on_delete=models.CASCADE)
    quantite = models.IntegerField(default = 1)
    date = models.DateField()
    statut = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.article.name}: {self.quantite}; statut: {self.statut}"
    
class Etudiant(models.Model):
    prenom = models.CharField(max_length=100)
    nom = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    Sexe = models.CharField(max_length=100)
    universite = models.CharField(max_length=100)
    departement = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    fac = models.CharField(max_length=100)
    niveau = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"

""" 
Les formulaires

"""
class CommandeForm(ModelForm):
    class Meta:
        model =  Commande
        fields = ["quantite"]
    
    
    
    
    
    
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'prix', 'image', 'stock', 'description']
        
CommandeFormSet = modelformset_factory(Commande, fields=('quantite',), extra=0, can_delete=True)