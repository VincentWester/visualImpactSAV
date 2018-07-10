# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, urllib, cStringIO

from PIL import Image
from io import BytesIO

from decimal import Decimal

from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# models part
from visualImpactSAV.models import Designation, SAV_file

class Pdf_generator(View):    
    def __init__(self, filename, title):
        self.filename = filename
        self.title = title

    def build_header(self, p):
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
        p.drawString(3*inch, 10.2*inch, self.title)

    def draw_table_one_column(self, height, length, alinea_title, alinea_lines, title, lines, p):
        size = len(lines)
        p.rect(-0.5*inch, height*inch, length*inch, (size * 0.2 + 0.5)*inch, fill=0)
        p.line(-0.5*inch, (height + 1)*inch, (length - 0.5)*inch, (height + 1)*inch)        
        p.setFont("Helvetica-Bold", 12)
        p.drawString(alinea_title*inch, (height + 1.1)*inch, title)
        p.setFont("Helvetica", 7)

        for i in range(size):
            p.drawString(alinea_lines*inch, (height + (i + 1)*0.2)*inch, lines[size - (i + 1)]) 

    def draw_description_part(self, height, p):        
        p.setFont("Helvetica-Bold", 12) 
        p.drawString(2.5*inch, (height)*inch, "Description du problème")
        p.setFont("Helvetica", 10)
        lines = self.sav_file.out_of_order_reason.split('\n')
        size = len(lines)
        for i in range(size):
            height = height - 0.3
            line = lines[i] if i == size - 1 else lines[i][:-1]
            p.drawString(-0.3*inch, height*inch, line)

    def get(self, request, pkSAVFile):
        self.sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
        filename_client_part = self.sav_file.name_client.replace(' ', '_') if self.sav_file.society_client == '' else self.sav_file.society_client.replace(' ', '_')
        final_filename = '{0}__{1}{2}'.format(self.filename, filename_client_part, '.pdf')

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(final_filename)

        buffer = BytesIO()
        p = canvas.Canvas(buffer)

        self.build_header(p)
        self.build_pdf(p)
        
        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()

        response.write(pdf)
        return response

class Pdf_generator_client(Pdf_generator): 
    def __init__(self):
        super(Pdf_generator_client, self).__init__('récapitulatif', 'Fiche SAV récapitulative')

    def build_pdf(self, p):
        height = 9.5

        sav_file = self.sav_file

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

        p.setFont("Helvetica-Bold", 12) 
        p.drawString(0.5*inch, (height + 1.1)*inch, "Adresse de facturation")
        p.drawString(4.5*inch, (height + 0)*inch, "Référence du produit")

        global_name_client = sav_file.name_client
        if sav_file.society_client:            
            global_name_client = sav_file.society_client + " - " + global_name_client 

        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, (height + 0.8)*inch, global_name_client)
        p.drawString(-0.3*inch, (height + 0.6)*inch, sav_file.street_client)
        p.drawString(-0.3*inch, (height + 0.4)*inch, sav_file.zipcode_client + " - " + sav_file.city_client)
        p.drawString(-0.3*inch, (height + 0.2)*inch, sav_file.email_client)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.3)*inch, "Marque : ")
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.3)*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.5)*inch, "Modèle : ")
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.5)*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.7)*inch, "N° série : ")
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.7)*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.9)*inch, "N° RMA : ")
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.9)*inch, sav_file.rma_number)

        height = height - 1.3 
        
        self.draw_description_part(height, p)

        lines = []
        lines.append("- Tout appareil remis en SAV doit être accompagné de la présente fiche de dépôt complétée datée et signée. Les pièces détachées ne sont ni reprises ni échangées.")
        lines.append("- Tout devis refusé fera l’objet d’une facturation de 90€ HT.")
        lines.append("- Sous réserve d’ensemble ou sous ensemble à changer en plus du montant indiqué ci-dessus qui n’auraient pas été décelés comme étant défectueux lors de l’élaboration.")
        lines.append("- Attention pour les dossiers comprenant des données stockées sous forme de carte ou de cassette aucune garantie de récupération n’est accordée.")
        self.draw_table_one_column(0.8, 7.6, 2, -0.4, "Conditions de prise en charge", lines, p)
        
        lines = []
        lines.append("Visual Impact France SAS au capital de 300000.00 euros")
        lines.append("74 Boulevard de Reuilly, 75012 Paris, France")
        lines.append("Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
        lines.append("No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")
        self.draw_table_one_column(-0.7, 7.6, 2, 2, "Informations complémentaires", lines, p)


class Pdf_generator_cost_estimate(Pdf_generator):
    def __init__(self):
        super(Pdf_generator_cost_estimate, self).__init__('devis-client', 'Offre commerciale')

    def build_pdf(self, p):   
        sav_file = self.sav_file

        p.setFont("Helvetica", 12)
        p.drawString(-0.5*inch, 9.6*inch, "Réference du fichier SAV : VIF-SAV-" + str(sav_file.id))

        p.setFont("Helvetica-Bold", 12)
        p.drawString(-0.3*inch, 9.1*inch, "Adresse de facturation")

        p.setFont("Helvetica", 10)
        global_name_client = sav_file.name_client
        if sav_file.society_client:            
            global_name_client = sav_file.society_client + " - " + global_name_client 

        p.drawString(-0.3*inch, 8.8*inch, global_name_client)
        p.drawString(-0.3*inch, 8.6*inch, sav_file.street_client)
        p.drawString(-0.3*inch, 8.4*inch, sav_file.zipcode_client + " - " + sav_file.city_client)
        p.drawString(-0.3*inch, 8.2*inch, sav_file.email_client)

        p.setFont("Helvetica-Bold", 12)

        p.drawString(4.5*inch, 7.8*inch, "Dossier suivi par : " + sav_file.registred_by.username)

        p.setFont("Helvetica", 10)

        p.drawString(4.5*inch, 7.5*inch, "Visual Impact France")
        p.drawString(4.5*inch, 7.3*inch, "74 boulevard de Reuilly")
        p.drawString(4.5*inch, 7.1*inch, "75012 - Paris")
        p.drawString(4.5*inch, 6.8*inch, sav_file.registred_by.email)


        p.rect(-0.5*inch, 5.9*inch, 7.2*inch, 0.8*inch, fill=0)
        p.setFont("Helvetica-Bold", 12)

        p.drawString(2.1*inch, 6.5*inch, "Référence du produit")
        p.line(-0.5*inch, 6.4*inch, 6.7*inch, 6.4*inch)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(-0.3*inch, 6.2*inch, "Marque : ")
        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, 6*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1.5*inch, 6.2*inch, "Modèle : ")
        p.setFont("Helvetica", 10)
        p.drawString(1.5*inch, 6*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, 6.2*inch, "N° série : ")
        p.setFont("Helvetica", 10)
        p.drawString(3.7*inch, 6*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5.5*inch, 6.2*inch, "N° suivi : ")
        p.setFont("Helvetica", 10)

        if sav_file.rma_number:     
            p.drawString(5.5*inch, 6*inch, sav_file.rma_number)
        else:
            p.drawString(5.5*inch, 6*inch,"Inconnu")



        p.setFont("Helvetica-Bold", 12)

        p.drawString(0*inch, 5.5*inch, "Désignation")
        p.drawString(4.8*inch, 5.5*inch, "Qté")
        p.drawString(5.8*inch, 5.5*inch, "Prix HT")
        p.line(-0.5*inch, 5.4*inch, 6.7*inch, 5.4*inch)

        p.setFont("Helvetica", 10)

        total = Decimal(0.0)
        height = 5.2
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

        lines = []
        lines.append("Banque : Societe Generale, Code Banque : 30003")
        lines.append("Code Guichet : 03190, Clé RIB : 12, Numero de Compte : 00020119192")
        lines.append("IBAN: FR76 3000 3031 9000 0201 1919 212, Code BICS : SOGEFRPP")
        lines.append("Titulaire du Compte : Visual Impact France")
        self.draw_table_one_column(height, 7.2, 2.5, 1.8, "Coordonnée", lines, p)
        
        height = height - 1.35

        lines = []
        lines.append("Visual Impact France SAS au capital de 300000.00 euros")
        lines.append("74 Boulevard de Reuilly, 75012 Paris, France")
        lines.append("Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
        lines.append("No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")
        self.draw_table_one_column(height, 7.2, 2, 1.8, "Informations complémentaires", lines, p)       
        

class Pdf_generator_furnisher(Pdf_generator):
    def __init__(self):
        super(Pdf_generator_furnisher, self).__init__('réparation', 'Demande de réparation')

    def build_pdf(self, p):

        sav_file = self.sav_file

        p.setFont("Helvetica", 12)
        p.drawString(-0.5*inch, 9.6*inch, "Réference du fichier SAV : VIF-SAV-" + str(sav_file.id))
        p.drawString(-0.5*inch, 9.4*inch, "Veuillez nous indiquer cette référence dans toutes nos correspondances.")

        p.setFont("Helvetica-Bold", 12)
        p.drawString(-0.3*inch, 8.7*inch, "Adresse du fournisseur")

        p.setFont("Helvetica", 10)
        furnisher = sav_file.furnisher

        p.drawString(-0.3*inch, 8.4*inch, furnisher.mark)
        p.drawString(-0.3*inch, 8.2*inch, furnisher.street + ", " + furnisher.complements)
        p.drawString(-0.3*inch, 8.0*inch, furnisher.zipcode + " - " + furnisher.city)
        p.drawString(-0.3*inch, 7.8*inch, furnisher.phone)


        p.setFont("Helvetica-Bold", 12)

        p.drawString(4.5*inch, 7.5*inch, "Dossier suivi par : " + sav_file.registred_by.username)

        p.setFont("Helvetica", 10)

        p.drawString(4.5*inch, 7.2*inch, "Visual Impact France")
        p.drawString(4.5*inch, 7*inch, "74 boulevard de Reuilly")
        p.drawString(4.5*inch, 6.8*inch, "75012 - Paris")
        p.drawString(4.5*inch, 6.6*inch, sav_file.registred_by.email)


        p.rect(-0.5*inch, 5.8*inch, 7.2*inch, 0.8*inch, fill=0)
        p.setFont("Helvetica-Bold", 12)

        p.drawString(2.1*inch, 6.4*inch, "Référence du produit")
        p.line(-0.5*inch, 6.4*inch, 6.7*inch, 6.4*inch)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(-0.3*inch, 6.1*inch, "Marque : ")
        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, 5.9*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1.5*inch, 6.1*inch, "Modèle : ")
        p.setFont("Helvetica", 10)
        p.drawString(1.5*inch, 5.9*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, 6.1*inch, "N° série : ")
        p.setFont("Helvetica", 10)
        p.drawString(3.7*inch, 5.9*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5.5*inch, 6.1*inch, "N° suivi : ")
        p.setFont("Helvetica", 10)

        if sav_file.rma_number:     
            p.drawString(5.5*inch, 5.9*inch, sav_file.rma_number)
        else:
            p.drawString(5.5*inch, 5.9*inch,"Inconnu")

        height = 5.4

        self.draw_description_part(height, p)

        lines = []
        lines.append("Visual Impact France SAS au capital de 300000.00 euros")
        lines.append("74 Boulevard de Reuilly, 75012 Paris, France")
        lines.append("Tel: +33 1 42 22 02 05, Fax: +33 1 42 22 02 85, vifrance@visualsfrance.com")
        lines.append("No TVA: FR72448429274, SIRET: 44842927400021, Code APE: 4643Z")
        self.draw_table_one_column(-0.7, 7.6, 2, 2, "Informations complémentaires", lines, p)     
        
