# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, urllib, cStringIO

from PIL import Image
from io import BytesIO

from decimal import Decimal

from django.http import HttpResponse
from django.conf import settings
from django.views.generic import DetailView
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# models part
from visualImpactSAV.models import Designation, SAV_file

def generate_pdf_name(sav_file):    
    filename = 'devis-client-'
    if not sav_file.society_client == '':
        filename = '{0}__{1}{2}'.format(filename, sav_file.society_client.replace(' ', '_'), '.pdf')
    else:
        filename = '{0}__{1}{2}'.format(filename, sav_file.name_client.replace(' ', '_'), '.pdf')

    return filename


#def send_pdf(request, pkSAVFile):
#    sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
#    filename = generate_pdf_name(sav_file)
#    pdf_string = build_pdf(request, sav_file)

#    file = open(filename, "wb")
#    file.write(pdf_string)
#    file.close()

#    subject = 'Votre Devis.'
#    message = 'Voici le devis SAV que vous avez demandé. \n Nous sommes heureux de vous compter parmi nos clients. \n Cordialement, \n {0}'.format(request.user.username)
    
#    from_email = sav_file.registred_by.email
#    to_list = [sav_file.registred_by.email, sav_file.email_client]

#    if not request.user.email == sav_file.registred_by.email:
#        to_list.append(request.user.email)

#    message = EmailMessage(subject, message, from_email, to_list)
#    message.attach_file(filename)
#    message.send()
    
#    os.remove(filename)

#    return redirect('visualImpactSAV:detailSAVFile', pkSAVFile)

def generate_pdf_client_cost_estimate(request, pkSAVFile):
    # Create the HttpResponse object with the appropriate PDF headers.
    sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
    filename = generate_pdf_name(sav_file)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    build_header(request, p, "Offre commerciale")
    build_pdf_client_cost_estimate(request, sav_file, p)
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

def generate_pdf_furnisher(request, pkSAVFile):
    # Create the HttpResponse object with the appropriate PDF headers.
    sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
    filename = generate_pdf_name(sav_file)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    build_header(request, p, "Demande de réparation")
    build_pdf_furnisher(request, sav_file, p)
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

def generate_pdf_client(request, pkSAVFile):
    # Create the HttpResponse object with the appropriate PDF headers.
    sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
    filename = generate_pdf_name(sav_file)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="{0}"'.format(filename)

    # Create the PDF object, using the BytesIO object as its "file."
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    build_header(request, p, "Fiche SAV récapitulative")  
    build_pdf_client(request, sav_file, p)  
    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)
    return response

def build_header(request, p, title):
    p.translate(inch,inch)
    url = os.path.join(settings.STATICFILES_DIRS[0], 'images/logoVisual.jpg')

    if not os.path.isfile(url):
        buffer.close()
        url_redirect = u"{% url 'visualImpactSAV:detailSAVFile' sav_file.id %}"
        return HttpResponse(render_to_string('djangoApp/errors/missingLogo.html', {'errors': "le logo de votre entreprise n'existe plus. Veuillez contacter le service technique. ", 'url': url_redirect }))

    logo = cStringIO.StringIO(urllib.urlopen(url).read())

    img = Image.open(logo)

    p.drawInlineImage(img, -0.7*inch, 10*inch, 122, 39)
    p.setFont("Helvetica-Bold", 20)
    p.drawString(3*inch, 10.2*inch, title)


def build_pdf_client_cost_estimate(request, sav_file, p):
    p.setFont("Helvetica", 12)
    p.drawString(-0.5*inch, 9.6*inch, "Réference du fichier SAV : VIF-SAV-" + str(sav_file.id))
    p.rect(-0.5*inch, 8*inch, 2.4*inch, 1.3*inch, fill=0)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(-0.3*inch, 9.1*inch, "Adresse de facturation")
    p.line(-0.5*inch,9*inch,1.9*inch,9*inch)

    p.setFont("Helvetica", 10)
    global_name_client = sav_file.name_client
    if sav_file.society_client:            
        global_name_client = sav_file.society_client + " - " + global_name_client 

    p.drawString(-0.3*inch, 8.8*inch, global_name_client)
    p.drawString(-0.3*inch, 8.6*inch, sav_file.street_client)
    p.drawString(-0.3*inch, 8.4*inch, sav_file.zipcode_client + " - " + sav_file.city_client)
    p.drawString(-0.3*inch, 8.1*inch, sav_file.email_client)


    p.rect(1.9*inch, 8*inch, 2.4*inch, 1.3*inch, fill=0)
    p.setFont("Helvetica-Bold", 12)

    p.drawString(2.1*inch, 9.1*inch, "Référence du produit")
    p.line(1.9*inch,9*inch,4.3*inch,9*inch)

    p.setFont("Helvetica", 10)

    p.drawString(2.1*inch, 8.8*inch, "Marque : " + sav_file.mark_product)
    p.drawString(2.1*inch, 8.6*inch, "Modèle : " + sav_file.name_product)
    p.drawString(2.1*inch, 8.4*inch, "N° série : " + sav_file.serial_number_product)
    if sav_file.tracking_number:     
        p.drawString(2.1*inch, 8.1*inch, "N° suivi : " + sav_file.tracking_number)


    p.rect(4.3*inch, 8*inch, 2.4*inch, 1.3*inch, fill=0)
    p.setFont("Helvetica", 12)

    p.drawString(4.5*inch, 9.1*inch, "Dossier suivi par : " + sav_file.registred_by.username)
    p.line(4.3*inch,9*inch,6.7*inch,9*inch)

    p.setFont("Helvetica", 10)

    p.drawString(4.5*inch, 8.8*inch, "Visual Studio")
    p.drawString(4.5*inch, 8.6*inch, "74 boulevard de Reuilly")
    p.drawString(4.5*inch, 8.4*inch, "75012 - Paris")
    p.drawString(4.5*inch, 8.1*inch, sav_file.registred_by.email)

    p.setFont("Helvetica-Bold", 12)

    p.drawString(0*inch, 7.1*inch, "Désignation")
    p.drawString(4.8*inch, 7.1*inch, "Qté")
    p.drawString(5.8*inch, 7.1*inch, "Prix HT")
    p.line(-0.5*inch,7*inch,6.7*inch,7*inch)

    p.setFont("Helvetica", 10)

    total = Decimal(0.0)
    height = 6.8
    i = 1

    designations = Designation.objects.all().filter(refered_SAV_file = sav_file).order_by('quantity')
    for designation in designations:
        height = height - 0.2
        p.drawString(-0.3*inch, height*inch, str(i) + "-")
        i += 1
        p.drawString(0*inch, height*inch, designation.designation)
        p.drawString(4.8*inch, height*inch, str(designation.quantity))
        p.drawString(5.8*inch, height*inch, str(designation.price) + " €")
        total += Decimal(designation.quantity) * Decimal(designation.price)

    height = height - 0.2
    p.line(4.5*inch,height*inch,6.7*inch,height*inch)
    height = height - 0.2

    p.setFont("Helvetica", 10)
    p.drawString(-0.3*inch, height*inch, "Tous nos prix s’entendent Hors Taxes et EXW PARIS.")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(4.5*inch, height*inch, "Prix total HT : ")
    p.drawString(5.8*inch, height*inch, str(round(total, 2)) + " €")
    height = height - 0.2        
    p.setFont("Helvetica", 10)
    p.drawString(-0.3*inch, height*inch, "Frais de transport sur demande sauf mention contraire.")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(4.5*inch, height*inch, "Taxe : ")
    p.drawString(5.8*inch, height*inch, "20%")
    height = height - 0.125   
    p.setFont("Helvetica", 5)
    p.drawString(-0.3*inch, height*inch, "Nous nous réservons la propriété des marchandises jusqu'au complet paiement du prix par l'acheteur.")
    height = height - 0.075
    p.drawString(-0.3*inch, height*inch, "Notre droit de revendication porte aussi bien sur les marchandises que sur leur prix si elles ont déjà été revendues.")
    height = height - 0.075
    p.drawString(-0.3*inch, height*inch, "En cas de retard de paiement aux termes fixés, les sommesdues porteront intérêt de plein droit et sans qu'il soit besoin d'une mise en demeure. ")
    height = height - 0.075
    p.drawString(-0.3*inch, height*inch, "La pénalité sera d'un montant égal à trois fois le taux d'intérêt légal (loi du 31/12/1992), sans que cette clause nuise à l'exigibilité de la dette.")
    height = height - 0.025
    p.setFont("Helvetica-Bold", 10)
    p.drawString(4.5*inch, height*inch, "Prix total TC : ")
    p.setFillColorRGB(1,0,0)
    p.drawString(5.8*inch, height*inch, str(round(total * Decimal(1.2), 2)) + " €")
    p.setFillColorRGB(0,0,0)
    height = height - 0.05
    p.rect(-0.5*inch, height*inch, 4.7*inch, 0.835*inch, fill=0)
    
    p.setFillColorRGB(1,0,0)
    height = height - 0.25
    p.setFont("Helvetica-Bold", 9)
    p.drawString(-0.3*inch, height*inch, "TOUT DEVIS REFUSE FERA L'OBJET D'UNE FACTURATION D'UNE SOMME FORFAITAIRE DE 95.00€ HT")
    height = height - 0.1
    p.rect(-0.5*inch, height*inch, 7.2*inch, 0.3*inch, fill=0)
    height = height - 0.225

    p.setFillColorRGB(0,0,0)
    p.setFont("Helvetica-Bold", 7)
    p.drawString(-0.3*inch, height*inch, "Delai de livraison : ")
    p.drawString(3.3*inch, height*inch, "Moyen de paiement : ")
    p.setFont("Helvetica", 7)
    p.drawString(0.9*inch, height*inch, "à confirmer")
    p.drawString(4.5*inch, height*inch, "à définir avant la commande")
    height = height - 0.125
    p.rect(-0.5*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)
    p.rect(3.1*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)

    p.setFillColorRGB(0,0,0)
    height = height - 1.35
    p.rect(-0.5*inch, height*inch, 3.6*inch, 1.3*inch, fill=0)
    p.line(-0.5*inch,(height + 1)*inch,3.1*inch,(height + 1)*inch)        
    p.setFont("Helvetica-Bold", 12)
    p.drawString(0*inch, (height + 1.1)*inch, "Informations complémentaires")
    p.setFont("Helvetica", 7)

    p.drawString(-0.3*inch, (height + 0.8)*inch, "Visual Impact France SAS au capital de 300000.00 euros")
    p.drawString(-0.3*inch, (height + 0.6)*inch, "74 Boulevard de Reuilly, 75012 Paris, France")
    p.drawString(-0.3*inch, (height + 0.4)*inch, "Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
    p.drawString(-0.3*inch, (height + 0.2)*inch, "No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")

    p.rect(3.1*inch, height*inch, 3.6*inch, 1.3*inch, fill=0)
    p.line(3.1*inch,(height + 1)*inch,6.7*inch,(height + 1)*inch)  
    p.setFont("Helvetica-Bold", 12)
    p.drawString(3.6*inch, (height + 1.1)*inch, "Coordonnées bancaires")
    p.setFont("Helvetica", 7)

    p.drawString(3.3*inch, (height + 0.8)*inch, "Banque : Societe Generale, Code Banque : 30003")
    p.drawString(3.3*inch, (height + 0.6)*inch, "Code Guichet : 03190, Clé RIB : 12, Numero de Compte : 00020119192")
    p.drawString(3.3*inch, (height + 0.4)*inch, "IBAN: FR76 3000 3031 9000 0201 1919 212, Code BICS : SOGEFRPP")
    p.drawString(3.3*inch, (height + 0.2)*inch, "Titulaire du Compte : Visual Impact France")       

def build_pdf_furnisher(request, sav_file, p):
    p.setFont("Helvetica", 12)
    p.drawString(-0.5*inch, 9.6*inch, "Réference du fichier SAV : VIF-SAV-" + str(sav_file.id))
    p.drawString(-0.5*inch, 9.4*inch, "Veuillez nous indiquer cette référence dans toutes nos correspondances.")
    p.rect(-0.5*inch, 7.6*inch, 2.4*inch, 1.3*inch, fill=0)

    p.setFont("Helvetica-Bold", 12)
    p.drawString(-0.3*inch, 8.7*inch, "Adresse du fournisseur")
    p.line(-0.5*inch,8.6*inch,1.9*inch,8.6*inch)

    p.setFont("Helvetica", 10)
    furnisher = sav_file.furnisher

    p.drawString(-0.3*inch, 8.4*inch, furnisher.mark)
    p.drawString(-0.3*inch, 8.2*inch, furnisher.street + ", " + furnisher.complements)
    p.drawString(-0.3*inch, 8.0*inch, furnisher.zipcode + " - " + furnisher.city)
    p.drawString(-0.3*inch, 7.7*inch, furnisher.phone)


    p.rect(1.9*inch, 7.6*inch, 2.4*inch, 1.3*inch, fill=0)
    p.setFont("Helvetica-Bold", 12)

    p.drawString(2.1*inch, 8.7*inch, "Référence du produit")
    p.line(1.9*inch,8.6*inch,4.3*inch,8.6*inch)

    p.setFont("Helvetica", 10)

    p.drawString(2.1*inch, 8.4*inch, "Marque : " + sav_file.mark_product)
    p.drawString(2.1*inch, 8.2*inch, "Modèle : " + sav_file.name_product)
    p.drawString(2.1*inch, 8.0*inch, "N° série : " + sav_file.serial_number_product)
    if sav_file.tracking_number:     
        p.drawString(2.1*inch, 7.7*inch, "N° suivi : " + sav_file.tracking_number)


    p.rect(4.3*inch, 7.6*inch, 2.4*inch, 1.3*inch, fill=0)
    p.setFont("Helvetica", 12)

    p.drawString(4.5*inch, 8.7*inch, "Dossier suivi par : " + sav_file.registred_by.username)
    p.line(4.3*inch,8.6*inch,6.7*inch,8.6*inch)

    p.setFont("Helvetica", 10)

    p.drawString(4.5*inch, 8.4*inch, "Visual Studio")
    p.drawString(4.5*inch, 8.2*inch, "74 boulevard de Reuilly")
    p.drawString(4.5*inch, 8.0*inch, "75012 - Paris")
    p.drawString(4.5*inch, 7.7*inch, sav_file.registred_by.email)

    p.setFont("Helvetica-Bold", 12)

    p.drawString(0*inch, 7.1*inch, "Désignation")
    p.drawString(5.8*inch, 7.1*inch, "Qté")
    p.line(-0.5*inch,7*inch,6.7*inch,7*inch)

    p.setFont("Helvetica", 10)

    total = Decimal(0.0)
    height = 6.8
    i = 1

    designations = Designation.objects.all().filter(refered_SAV_file = sav_file).order_by('quantity')
    for designation in designations:
        height = height - 0.2
        p.drawString(-0.3*inch, height*inch, str(i) + "-")
        i += 1
        p.drawString(0*inch, height*inch, designation.designation)
        p.drawString(5.8*inch, height*inch, str(designation.quantity))

    p.setFillColorRGB(0,0,0)
    height = height - 1.55
    p.rect(-0.5*inch, height*inch, 7.6*inch, 1.3*inch, fill=0)
    p.line(-0.5*inch, (height + 1)*inch, 7.1*inch, (height + 1)*inch)        
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*inch, (height + 1.1)*inch, "Informations complémentaires")
    p.setFont("Helvetica", 7)

    p.drawString(2*inch, (height + 0.8)*inch, "Visual Impact France SAS au capital de 300000.00 euros")
    p.drawString(2*inch, (height + 0.6)*inch, "74 Boulevard de Reuilly, 75012 Paris, France")
    p.drawString(2*inch, (height + 0.4)*inch, "Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
    p.drawString(2*inch, (height + 0.2)*inch, "No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")       

def build_pdf_client(request, sav_file, p):
    height = 9.5

    p.setFont("Helvetica-Bold", 12)
    p.drawString(-0.5*inch, height*inch, "Référence : ")
    p.setFont("Helvetica", 12)
    p.drawString(0.5*inch, height*inch, "VIF-SAV-" + str(sav_file.id))
    p.setFont("Helvetica-Bold", 12)
    p.drawString(3.7*inch, height*inch, "Suivi par : ")
    p.setFont("Helvetica", 12)
    p.drawString(4.7*inch, height*inch, sav_file.registred_by.username)
    p.setFont("Helvetica-Bold", 12)
    p.drawString(-0.5*inch, (height - 0.3)*inch, "Nom du client : ")
    p.setFont("Helvetica", 12)
    p.drawString(0.8*inch, (height - 0.3)*inch, sav_file.name_client)
    height = height - 1.8 

    p.rect(-0.5*inch, height*inch, 7.6*inch, 1.3*inch, fill=0)
    p.line(-0.5*inch, (height + 1)*inch, 7.1*inch, (height + 1)*inch)    
    p.line(3.5*inch, height*inch, 3.5*inch, (height + 1.3)*inch)       
    p.setFont("Helvetica-Bold", 12) 
    p.drawString(0.5*inch, (height + 1.1)*inch, "Adresse de facturation")
    p.drawString(4.5*inch, (height + 1.1)*inch, "Référence du produit")

    global_name_client = sav_file.name_client
    if sav_file.society_client:            
        global_name_client = sav_file.society_client + " - " + global_name_client 

    p.setFont("Helvetica", 10)
    p.drawString(-0.3*inch, (height + 0.8)*inch, global_name_client)
    p.drawString(-0.3*inch, (height + 0.6)*inch, sav_file.street_client)
    p.drawString(-0.3*inch, (height + 0.4)*inch, sav_file.zipcode_client + " - " + sav_file.city_client)
    p.drawString(-0.3*inch, (height + 0.2)*inch, sav_file.email_client)

    p.setFont("Helvetica-Bold", 10)
    p.drawString(3.7*inch, (height + 0.8)*inch, "Marque : ")
    p.setFont("Helvetica", 10)
    p.drawString(4.5*inch, (height + 0.8)*inch, sav_file.mark_product)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(3.7*inch, (height + 0.6)*inch, "Modèle : ")
    p.setFont("Helvetica", 10)
    p.drawString(4.5*inch, (height + 0.6)*inch, sav_file.name_product)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(3.7*inch, (height + 0.4)*inch, "N° série : ")
    p.setFont("Helvetica", 10)
    p.drawString(4.5*inch, (height + 0.4)*inch, sav_file.serial_number_product)
    if sav_file.tracking_number:     
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height + 0.2)*inch, "N° suivi : ")
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height + 0.2)*inch, sav_file.tracking_number)

    height = height - 0.3 
    
    p.setFont("Helvetica-Bold", 12) 
    p.drawString(2.5*inch, (height)*inch, "Description du problème")
    p.setFont("Helvetica", 10)
    p.drawString(-0.3*inch, (height - 0.3)*inch, sav_file.out_of_order_reason)

    height = height - 7.8 
    
    p.rect(-0.5*inch, height*inch, 7.6*inch, 1.3*inch, fill=0)
    p.line(-0.5*inch, (height + 1)*inch, 7.1*inch, (height + 1)*inch)        
    p.setFont("Helvetica-Bold", 12)
    p.drawString(2*inch, (height + 1.1)*inch, "Informations complémentaires")
    p.setFont("Helvetica", 7)

    p.drawString(2*inch, (height + 0.8)*inch, "Visual Impact France SAS au capital de 300000.00 euros")
    p.drawString(2*inch, (height + 0.6)*inch, "74 Boulevard de Reuilly, 75012 Paris, France")
    p.drawString(2*inch, (height + 0.4)*inch, "Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
    p.drawString(2*inch, (height + 0.2)*inch, "No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")    

