from django.shortcuts import render
from utilisateur.models import Utilisateur
from general.models import CommandeForm,CommandeFormSet, Etudiant,  Personne, ArticleForm, Article, Commande
from django.contrib.auth import login
from django.shortcuts import redirect
import datetime
from django.core.mail import BadHeaderError, send_mail
# Create your views here.

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import openpyxl
from django.http import HttpResponse



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
    return render(request , 'general/accueil.html',{"articles":articles, 'panier':nbrecommandes(request)} )


def inscription(request):
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
    return render(request , 'general/inscription.html',{'inscrit':False, 'message': False} )

def newPersonne(request):
    prenom = request.POST['first_name']
    nom = request.POST['last_name']
    village = request.POST['adresse']
    sexe = request.POST['sexe']
    universite = request.POST['universite']
    fac = request.POST['fac']
    departement = request.POST['dep']
    niveau =  request.POST['niveau']
    email = request.POST['email']
    message = False
    if Etudiant.objects.filter(email=email).exists():
        message = True
    else:
        etudiant = Etudiant.objects.get_or_create(prenom = prenom, nom = nom, village=village, Sexe=sexe, universite= universite, fac=fac, departement=departement, niveau=niveau, email=email)
    return render(request , 'general/inscription.html', {'inscrit':True, 'message':message })

def addarticle(request):
    form = ArticleForm()
       # user = Utilisateur.objects.create_user('bil1', 'bil1@gmail.com', 'bil123456', first_name='Bilali1', last_name='Diallo')
    return render(request , 'general/newarticle.html', {"form": form, 'panier':nbrecommandes(request)})

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
    etudiants= Etudiant.objects.all()
    nbr = len(etudiants)
    nbrH = len([i for i in etudiants if i.Sexe=='M'])
    nbrF = len([i for i in etudiants if i.Sexe=='F'])
    return render(request , 'general/panier.html', {'etudiants':etudiants, 'nbr':nbr , 'nbrH':nbrH, 'nbrF':nbrF})

def confirmPanier(request):
    personne = Personne.objects.get(user = request.user)
    prix = 0
    commandes = []
    if request.method == 'POST':
        formset = CommandeFormSet(request.POST, queryset=Commande.objects.filter(acheteur= personne))
        if formset.is_valid():
            formset.save()
            
            commandes = Commande.objects.filter(acheteur= personne, statut = False)
            for commande in commandes:
                    commande.statut = True
                    commande.save()
                    prix += commande.article.prix*commande.quantite
            send_email(personne, prix)
            
        else:
            # Affichez les erreurs dans la console pour déboguer
            print(formset.errors)
            
        
    return  render(request , 'general/panier.html', {'source': 'comfirme', 'commandes':commandes, 'prix':prix, 'panier':nbrecommandes(request)})



def commander(request, id):
    user = request.user 
    personne = Personne.objects.get(user = user)
    article  = Article.objects.get(id = id)
    commande =  Commande.objects.get_or_create(article=article, acheteur= personne, date= datetime.datetime.now(),statut = False)
    return redirect('panier')








        
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
   
   
def nbrecommandes(request):
    if request.user.is_authenticated:
        user = request.user
        personne = Personne.objects.get(user = user)
        return len(Commande.objects.filter(acheteur= personne, statut = False))
    return 0



def download_etudiants_pdf(request):
    # Créer une réponse HTTP avec type de contenu PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="etudiants.pdf"'

    # Créer un document PDF
    doc = SimpleDocTemplate(response, pagesize=A4)
    
    # Styles pour le PDF
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    body_style = styles['BodyText']

    # Titre du document
    title = Paragraph("Liste des Étudiants", title_style)

    # Récupérer les étudiants depuis la base de données
    etudiants = Etudiant.objects.all()

    # Calculer les statistiques des étudiants
    total_etudiants = etudiants.count()
    total_hommes = etudiants.filter(Sexe__iexact='M').count()
    total_femmes = etudiants.filter(Sexe__iexact='F').count()

    pourcentage_hommes = (total_hommes / total_etudiants) * 100 if total_etudiants > 0 else 0
    pourcentage_femmes = (total_femmes / total_etudiants) * 100 if total_etudiants > 0 else 0

    stats_text = f"Total Étudiants: {total_etudiants}<br/>Total Hommes: {total_hommes} ({pourcentage_hommes:.2f}%)<br/>Total Femmes: {total_femmes} ({pourcentage_femmes:.2f}%)"
    stats_paragraph = Paragraph(stats_text, body_style)

    # Créer un tableau pour les données des étudiants
    data = [['Prénom', 'Nom', 'Village', 'Sexe', 'Université',  'Niveau']]
    
    for etudiant in etudiants:
        data.append([etudiant.prenom, etudiant.nom, etudiant.village, etudiant.Sexe, etudiant.universite+'\n'+etudiant.fac+'\n'+etudiant.departement, etudiant.niveau])
    
    # Créer un tableau ReportLab
    table = Table(data)
    
    # Ajouter du style au tableau
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table.setStyle(style)
    
    # Construire le document PDF
    elements = [title, Spacer(1, 12), stats_paragraph, Spacer(1, 12), table]
    doc.build(elements)
    
    return response




def download_etudiants_excel(request):
    # Créer un classeur Excel
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Etudiants"

    # Écrire l'en-tête
    headers = ['Prénom', 'Nom', 'Village', 'Sexe', 'Université', 'Département', 'Fac', 'Niveau']
    ws.append(headers)

    # Récupérer les étudiants depuis la base de données
    etudiants = Etudiant.objects.all()

    # Écrire les données des étudiants dans le fichier Excel
    for etudiant in etudiants:
        ws.append([etudiant.prenom, etudiant.nom, etudiant.village, etudiant.Sexe, etudiant.universite, etudiant.departement, etudiant.fac, etudiant.niveau])

    # Créer une réponse HTTP avec type de contenu Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="etudiants.xlsx"'

    # Sauvegarder le classeur dans la réponse
    wb.save(response)
    return response