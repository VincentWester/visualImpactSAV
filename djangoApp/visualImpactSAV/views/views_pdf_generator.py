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
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# models part
from visualImpactSAV.models import Designation, SAV_file

def generate_pdf(request, pkSAVFile):
        # Create the HttpResponse object with the appropriate PDF headers.
        sav_file = get_object_or_404(SAV_file, id = pkSAVFile)
        designations = Designation.objects.all().filter(refered_SAV_file = sav_file).order_by('quantity')
        
        filename = "devis-client-"
        if not sav_file.society_client == '':
            filename = "{0}{1}".format(filename, sav_file.society_client)
        else:
            filename = "{0}{1}".format(filename, sav_file.name_client.replace(' ', '_'))


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}.pdf"'.format(filename)

        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(buffer)
        #canvas.setTitle("Offre commercial")
        p.translate(inch,inch)

        url = os.path.join(settings.STATICFILES_DIRS[0], 'images/logoVisual.jpg')

        if not os.path.isfile(url):
            buffer.close()
            url_redirect = u"{% url 'visualImpactSAV:detailSAVFile' sav_file.id %}"
            return HttpResponse(render_to_string('djangoApp/errors/missingLogo.html', {'errors': "le logo de votre entreprise n'existe plus. Veuillez contacter le service technique. ", 'url': url_redirect }))

        file = cStringIO.StringIO(urllib.urlopen(url).read())

        img = Image.open(file)

        p.drawInlineImage(img, -0.7*inch, 10*inch, 122, 39)
        p.setFont("Helvetica-Bold", 20)
        p.drawString(3*inch, 10.2*inch, "Offre commerciale")
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.rect(-0.5*inch, 8*inch, 2.4*inch, 1.3*inch, fill=0)

        p.setFont("Helvetica", 12)
        p.drawString(-0.5*inch, 9.6*inch, "Réference du fichier SAV : " + str(sav_file.id))

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

        p.drawString(4.5*inch, 9.1*inch, "Dossier suivi par : NomUser")
        p.line(4.3*inch,9*inch,6.7*inch,9*inch)

        p.setFont("Helvetica", 10)

        p.drawString(4.5*inch, 8.8*inch, "Visual Studio")
        p.drawString(4.5*inch, 8.6*inch, "74 boulevard de Reuilly")
        p.drawString(4.5*inch, 8.4*inch, "75012 - Paris")
        p.drawString(4.5*inch, 8.1*inch, "Contact email : email@User.fr")


        p.setFont("Helvetica-Bold", 12)

        p.drawString(0*inch, 7.1*inch, "Désignation")
        p.drawString(4.8*inch, 7.1*inch, "Qté")
        p.drawString(5.8*inch, 7.1*inch, "Prix HT")
        p.line(-0.5*inch,7*inch,6.7*inch,7*inch)

        p.setFont("Helvetica", 10)

        total = Decimal(0.0)
        height = 6.8
        i = 1
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
        height = height - 0.085   
        p.setFont("Helvetica", 5)
        p.drawString(-0.3*inch, height*inch, "Nous nous réservons la propriété des marchandises jusqu'au complet paiement du prix par l'acheteur.")
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, "Notre droit de revendication porte aussi bien sur les marchandises que sur leur prix si elles ont déjà été revendues.")
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, "En cas de retard de paiement aux termes fixés, les sommesdues porteront intérêt de plein droit et sans qu'il soit besoin d'une mise en demeure. ")
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, "La pénalité sera d'un montant égal à trois fois le taux d'intérêt légal (loi du 31/12/1992), sans que cette clause nuise à l'exigibilité de la dette.")
        height = height - 0.075
        p.setFont("Helvetica-Bold", 5)
        p.drawString(-0.3*inch, height*inch, "TOUT DEVIS REFUSE FERA L'OBJET D'UNE FACTURATION D'UNE SOMME FORFAITAIRE DE 95.00€ HT.")
        p.setFont("Helvetica-Bold", 10)
        p.drawString(4.5*inch, height*inch, "Prix total TC : ")
        p.setFillColorRGB(1,0,0)
        p.drawString(5.8*inch, height*inch, str(round(total * Decimal(1.2), 2)) + " €")


        p.setFillColorRGB(0,0,0)
        height = height - 0.05
        p.rect(-0.5*inch, height*inch, 4.7*inch, 0.835*inch, fill=0)
        height = height - 0.225
        p.setFont("Helvetica-Bold", 7)
        p.drawString(-0.3*inch, height*inch, "Delai de livraison : ")
        p.drawString(3.3*inch, height*inch, "Moyen de paiement : ")
        p.setFont("Helvetica", 7)
        p.drawString(0.9*inch, height*inch, "à confirmer")
        p.drawString(4.5*inch, height*inch, "à définir avant la commande")
        height = height - 0.125
        p.rect(-0.5*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)
        p.rect(3.1*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)


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

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response