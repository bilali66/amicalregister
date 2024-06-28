from django.contrib import admin
from .models import Commande, Personne, Article
# Register your models here.


admin.site.register(Article) 
admin.site.register(Commande) 
admin.site.register(Personne) 