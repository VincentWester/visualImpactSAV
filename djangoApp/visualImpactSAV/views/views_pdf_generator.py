# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import urllib
import cStringIO

from PIL import Image
from io import BytesIO
from decimal import Decimal
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

from django.utils.translation import ugettext as _
from django.http import HttpResponse
from django.conf import settings
from django.views import View
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
# from django.core.mail import EmailMessage

from visualImpactSAV.models import Designation, SAV_file


field_separator = " : "
normal_separator = " - "
coma_separator = ", "  # les 3 en constantes


class Pdf_generator(View):
    def __init__(self, filename, title):
        self.filename = filename
        self.title = title

    def build_header(self, p):
        p.translate(inch, inch)
        url = os.path.join(settings.STATICFILES_DIRS[0], 'images/logoVisual.jpg')

        if not os.path.isfile(url):
            buffer.close()
            url_redirect = "{% url 'visualImpactSAV:detailSAVFile' sav_file.id %}"
            return HttpResponse(
                render_to_string(
                    'djangoApp/errors/missingLogo.html',
                    {
                        'errors': _("Logo Error"),
                        'url': url_redirect
                    }
                )
            )

        logo = cStringIO.StringIO(urllib.urlopen(url).read())

        img = Image.open(logo)

        p.drawInlineImage(img, -0.7*inch, 10*inch, 122, 39)
        p.setFont("Helvetica-Bold", 20)
        print self.title
        p.drawString(3*inch, 10.2*inch, self.title)

    def draw_table_one_column(self, height, length, alinea_title, alinea_lines, title, lines, p):
        height_column = len(lines) * 0.2
        p.rect(-0.5*inch, height*inch, length*inch, (height_column + 0.5)*inch, fill=0)
        p.line(-0.5*inch, (height + 1)*inch, (length - 0.5)*inch, (height + 1)*inch)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(alinea_title*inch, (height + 1.1)*inch, title)
        p.setFont("Helvetica", 7)

        for line in lines:
            p.drawString(alinea_lines*inch, (height + height_column)*inch, line)
            height_column -= 0.2

    def draw_description_part(self, height, p):
        p.setFont("Helvetica-Bold", 12)
        # "Description du problème"
        p.drawString(2.5*inch, (height)*inch, _("Problems' description"))
        p.setFont("Helvetica", 10)
        lines = self.sav_file.out_of_order_reason.split('\n')
        size = len(lines)
        for i in range(size):
            height = height - 0.3
            line = lines[i] if i == size - 1 else lines[i][:-1]
            p.drawString(-0.3*inch, height*inch, line)

    def get(self, request, pkSAVFile):
        self.sav_file = get_object_or_404(SAV_file, id=pkSAVFile)

        filename_customer_part = ''
        if self.sav_file.society_client == '':
            filename_customer_part = self.sav_file.name_client.replace(' ', '_')
        else:
            filename_customer_part = self.sav_file.society_client.replace(' ', '_')

        final_filename = '{0}__{1}{2}'.format(self.filename, filename_customer_part, '.pdf')

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
        # récapitulatif, Fiche SAV récapitulative
        super(Pdf_generator_client, self).__init__(_("customer-summary"), _("Summary after sell sheet"))

    def build_pdf(self, p):
        height = 9.5

        sav_file = self.sav_file
        global_name_client = sav_file.name_client

        p.setFont("Helvetica-Bold", 12)
        # Référence
        p.drawString(-0.5*inch, height*inch, _("Reference") + field_separator)
        p.setFont("Helvetica", 12)
        # VIF-SAV-
        p.drawString(0.5*inch, height*inch, _("VIF-AS-") + str(sav_file.id))
        p.setFont("Helvetica-Bold", 12)
        # Crée le
        p.drawString(3.7*inch, height*inch, ("Created at") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(5*inch, height*inch, sav_file.creation_date.strftime("%d/%m/%Y %H:%M"))
        p.setFont("Helvetica-Bold", 12)
        # Suivi par
        p.drawString(-0.5*inch, (height - 0.3)*inch, _("Managed by") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(0.5*inch, (height - 0.3)*inch, sav_file.registred_by.username)
        p.setFont("Helvetica-Bold", 12)
        # Nom du client
        p.drawString(3.7*inch, (height - 0.3)*inch, _("Customer name") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(5*inch, (height - 0.3)*inch, global_name_client)
        height = height - 1.8

        p.setFont("Helvetica-Bold", 12)
        # Adresse de facturation
        p.drawString(0.5*inch, (height + 1.1)*inch, _("Billing address"))
        # Référence du produit
        p.drawString(4.5*inch, (height + 0)*inch, _("Product reference"))

        if sav_file.society_client:
            global_name_client = sav_file.society_client + normal_separator + global_name_client

        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, (height + 0.8)*inch, global_name_client)
        p.drawString(-0.3*inch, (height + 0.6)*inch, sav_file.street_client)
        p.drawString(-0.3*inch, (height + 0.4)*inch, sav_file.zipcode_client + normal_separator + sav_file.city_client)
        p.drawString(-0.3*inch, (height + 0.2)*inch, sav_file.email_client)

        p.setFont("Helvetica-Bold", 10)
        # Marque
        p.drawString(3.7*inch, (height - 0.3)*inch, _("Brand") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.3)*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        # Modèle
        p.drawString(3.7*inch, (height - 0.5)*inch, _("Model") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.5)*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        # N° série
        p.drawString(3.7*inch, (height - 0.7)*inch, _("Serial number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.7)*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        # N° RMA
        p.drawString(3.7*inch, (height - 0.9)*inch, _("RMA number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.9)*inch, sav_file.rma_number)

        height = height - 1.3

        self.draw_description_part(height, p)

        lines = [_("AS condition 1"), _("AS condition 2"), _("AS condition 3"), _("AS condition 4")]
        self.draw_table_one_column(0.8, 7.6, 2, -0.4, _("Conditions"), lines, p)

        lines = [_("VI Addr name-capital-social"), _("VI Addr street-zipcode"), _("VI Addr phone-mail"), _("VI Infos")]
        self.draw_table_one_column(-0.7, 7.6, 2, 2, _("Added informations"), lines, p)


class Pdf_generator_cost_estimate(Pdf_generator):
    def __init__(self):
        # devis-client, Offre commerciale
        super(Pdf_generator_cost_estimate, self).__init__(_("cost-estimate"), _("Commercial offer"))

    def build_pdf(self, p):
        sav_file = self.sav_file

        p.setFont("Helvetica", 12)
        as_file_reference = _("AS file reference") + field_separator + _("VIF-AS-") + str(sav_file.id)
        p.drawString(-0.5*inch, 9.6*inch, as_file_reference)
        p.setFont("Helvetica-Bold", 12)
        # Adresse de facturation
        p.drawString(-0.3*inch, 9.1*inch, _("Billing address"))

        p.setFont("Helvetica", 10)
        global_name_client = sav_file.name_client
        if sav_file.society_client:
            global_name_client = sav_file.society_client + normal_separator + global_name_client

        p.drawString(-0.3*inch, 8.8*inch, global_name_client)
        p.drawString(-0.3*inch, 8.6*inch, sav_file.street_client)
        p.drawString(-0.3*inch, 8.4*inch, sav_file.zipcode_client + normal_separator + sav_file.city_client)
        p.drawString(-0.3*inch, 8.2*inch, sav_file.email_client)

        p.setFont("Helvetica-Bold", 12)
        # Dossier suivi par
        p.drawString(4.5*inch, 7.8*inch, _("File managed by") + field_separator + sav_file.registred_by.username)

        p.setFont("Helvetica", 10)

        # "Visual Impact France"
        p.drawString(4.5*inch, 7.5*inch, _("VI Addr name"))
        # "74 boulevard de Reuilly"
        p.drawString(4.5*inch, 7.3*inch, _("VI Addr street"))
        # "75012 - Paris"
        p.drawString(4.5*inch, 7.1*inch, _("VI Addr zipcode"))
        p.drawString(4.5*inch, 6.8*inch, sav_file.registred_by.email)

        p.rect(-0.5*inch, 5.9*inch, 7.2*inch, 0.8*inch, fill=0)
        p.setFont("Helvetica-Bold", 12)

        # Référence du produit
        p.drawString(2.1*inch, 6.5*inch, _("Product reference"))
        p.line(-0.5*inch, 6.4*inch, 6.7*inch, 6.4*inch)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(-0.3*inch, 6.2*inch, _("Brand") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, 6*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1.5*inch, 6.2*inch, _("Model") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(1.5*inch, 6*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, 6.2*inch, _("Serial number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(3.7*inch, 6*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5.5*inch, 6.2*inch, _("RMA number") + field_separator)
        p.setFont("Helvetica", 10)

        if sav_file.rma_number:
            p.drawString(5.5*inch, 6*inch, sav_file.rma_number)
        else:
            p.drawString(5.5*inch, 6*inch, _("Unknown"))

        p.setFont("Helvetica-Bold", 12)

        p.drawString(0*inch, 5.5*inch, _("Designations"))
        p.drawString(4.8*inch, 5.5*inch, _("Quantity"))
        p.drawString(5.8*inch, 5.5*inch, _("Pre-tax price"))
        p.line(-0.5*inch, 5.4*inch, 6.7*inch, 5.4*inch)

        p.setFont("Helvetica", 10)

        total = Decimal(0.0)
        height = 5.2
        # Doute : trouver un moyen de choper le compteur d'une boucle for
        i = 1

        # Doute : peut-être arriver à un moyen avec moins de requêtes
        designations = Designation.objects.all().filter(refered_SAV_file=sav_file)
        for designation in designations:
            height = height - 0.2
            p.drawString(-0.3*inch, height*inch, str(i) + normal_separator)
            i += 1
            p.drawString(0*inch, height*inch, designation.designation)
            p.drawString(4.8*inch, height*inch, str(designation.quantity))
            p.drawString(5.8*inch, height*inch, str(designation.price) + _(" £"))
            total += Decimal(designation.quantity) * Decimal(designation.price)

        height = height - 0.2
        p.line(4.5*inch, height*inch, 6.7*inch, height*inch)
        height = height - 0.2

        p.setFont("Helvetica", 10)
        # "Tous nos prix s’entendent Hors Taxes et EXW PARIS."
        p.drawString(-0.3*inch, height*inch, _("All our prices are given as excluding tax"))
        p.setFont("Helvetica-Bold", 10)
        p.drawString(4.5*inch, height*inch, _("Total pre-tax price") + field_separator)
        p.drawString(5.8*inch, height*inch, str(round(total, 2)).encode('utf8') + _(" £"))
        height = height - 0.2
        p.setFont("Helvetica", 10)
        # Frais de transport sur demande sauf mention contraire.
        p.drawString(-0.3*inch, height*inch, _("Transport fees when asked except where otherwise specified"))
        p.setFont("Helvetica-Bold", 10)
        # Taxe
        p.drawString(4.5*inch, height*inch, ("Tax") + field_separator)
        # 20%
        p.drawString(5.8*inch, height*inch, _("Tax percent"))
        height = height - 0.125
        p.setFont("Helvetica", 5)
        p.drawString(-0.3*inch, height*inch, _("Buying condition 1"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 2"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 3"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 4"))
        height = height - 0.025
        p.setFont("Helvetica-Bold", 10)
        # Prix total TC
        p.drawString(4.5*inch, height*inch, _("Total price AI") + field_separator)
        p.setFillColorRGB(1, 0, 0)
        p.drawString(5.8*inch, height*inch, str(round(total * Decimal(1.2), 2)).encode('utf8') + _(" £"))
        p.setFillColorRGB(0, 0, 0)
        height = height - 0.05
        p.rect(-0.5*inch, height*inch, 4.7*inch, 0.835*inch, fill=0)

        p.setFillColorRGB(1, 0, 0)
        height = height - 0.25
        p.setFont("Helvetica-Bold", 9)
        # TOUT DEVIS REFUSE FERA L'OBJET D'UNE FACTURATION D'UNE SOMME FORFAITAIRE DE 95.00€ HT
        p.drawString(-0.3*inch, height*inch, _("ALL REFUSED COST ESTIMATE WILL BE FACTURED 90£ (TAX EXCLUDED)"))
        height = height - 0.1
        p.rect(-0.5*inch, height*inch, 7.2*inch, 0.3*inch, fill=0)
        height = height - 0.225

        p.setFillColorRGB(0, 0, 0)
        p.setFont("Helvetica-Bold", 7)
        # Delai de livraison
        p.drawString(-0.3*inch, height*inch, _("Delivery time") + field_separator)
        # Moyen de paiement
        p.drawString(3.3*inch, height*inch, _("Means of payment") + field_separator)
        p.setFont("Helvetica", 7)
        # à confirmer
        p.drawString(0.9*inch, height*inch, _("to confirm"))
        # à définir avant la commande
        p.drawString(4.5*inch, height*inch, _("to define before the command"))
        height = height - 0.125
        p.rect(-0.5*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)
        p.rect(3.1*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)

        p.setFillColorRGB(0, 0, 0)
        height = height - 1.35

        lines = [_("VI bank-code bank"), _("VI RIB"), _("VI IBAN"), _("VI account owner")]
        self.draw_table_one_column(height, 7.2, 2.5, 1.8, _("Bank details"), lines, p)

        height = height - 1.35

        lines = [_("VI Addr name-capital-social"), _("VI Addr street-zipcode"), _("VI Addr phone-mail"), _("VI Infos")]
        self.draw_table_one_column(height, 7.2, 2, 1.8, _("Added informations"), lines, p)


class Pdf_generator_furnisher(Pdf_generator):
    def __init__(self):
        # réparations, Demande de réparation
        super(Pdf_generator_furnisher, self).__init__(_("repairs"), _("Repairs asking"))

    def build_pdf(self, p):

        sav_file = self.sav_file

        p.setFont("Helvetica", 12)
        p.drawString(-0.5*inch, 9.6*inch, _("AS file reference") + field_separator + _("VIF-AS-") + str(sav_file.id))
        # "Veuillez nous indiquer cette référence dans toutes nos correspondances."
        p.drawString(-0.5*inch, 9.4*inch, _("Please, tell this reference number in all our correspondances."))

        p.setFont("Helvetica-Bold", 12)
        p.drawString(-0.3*inch, 8.7*inch, _("Billing address"))

        p.setFont("Helvetica", 10)
        furnisher = sav_file.furnisher

        p.drawString(-0.3*inch, 8.4*inch, furnisher.mark)
        p.drawString(-0.3*inch, 8.2*inch, furnisher.street + coma_separator + furnisher.complements)
        p.drawString(-0.3*inch, 8.0*inch, furnisher.zipcode + field_separator + furnisher.city)
        p.drawString(-0.3*inch, 7.8*inch, furnisher.phone)

        p.setFont("Helvetica-Bold", 12)

        p.drawString(4.5*inch, 7.5*inch, _("File managed by") + field_separator + sav_file.registred_by.username)

        p.setFont("Helvetica", 10)

        p.drawString(4.5*inch, 7.2*inch, _("VI Addr name"))
        p.drawString(4.5*inch, 7*inch, _("VI Addr street"))
        p.drawString(4.5*inch, 6.8*inch, _("VI Addr zipcode"))
        p.drawString(4.5*inch, 6.6*inch, sav_file.registred_by.email)

        p.rect(-0.5*inch, 5.8*inch, 7.2*inch, 0.8*inch, fill=0)
        p.setFont("Helvetica-Bold", 12)

        p.drawString(2.1*inch, 6.4*inch, _("Product reference"))
        p.line(-0.5*inch, 6.4*inch, 6.7*inch, 6.4*inch)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(-0.3*inch, 6.1*inch, _("Brand") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, 5.9*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(1.5*inch, 6.1*inch, _("Model") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(1.5*inch, 5.9*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, 6.1*inch, _("Serial number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(3.7*inch, 5.9*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(5.5*inch, 6.1*inch, _("RMA number") + field_separator)
        p.setFont("Helvetica", 10)

        if sav_file.rma_number:
            p.drawString(5.5*inch, 5.9*inch, sav_file.rma_number)
        else:
            p.drawString(5.5*inch, 5.9*inch, _("Unknown"))

        height = 5.4

        self.draw_description_part(height, p)

        lines = [_("VI Addr name-capital-social"), _("VI Addr street-zipcode"), _("VI Addr phone-mail"), _("VI Infos")]
        self.draw_table_one_column(-0.7, 7.6, 2, 2, _("Added informations"), lines, p)


class Pdf_answer_reparation(Pdf_generator):
    def __init__(self):
        # 'retour-réparation', 'Retour réparation'
        super(Pdf_answer_reparation, self).__init__(_("repairs-return"), _("Repairs return"))

    def build_pdf(self, p):
        height = 9.5

        sav_file = self.sav_file

        p.setFont("Helvetica-Bold", 12)
        p.drawString(-0.5*inch, height*inch, _("Reference") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(0.5*inch, height*inch, _("VIF-AS-") + str(sav_file.id))
        p.setFont("Helvetica-Bold", 12)
        p.drawString(3.7*inch, height*inch, _("Managed by") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(4.7*inch, height*inch, sav_file.registred_by.username)
        p.setFont("Helvetica-Bold", 12)
        p.drawString(-0.5*inch, (height - 0.3)*inch, _("Customer name") + field_separator)
        p.setFont("Helvetica", 12)
        p.drawString(0.8*inch, (height - 0.3)*inch, sav_file.name_client)
        height = height - 1.8

        p.setFont("Helvetica-Bold", 12)
        p.drawString(0.5*inch, (height + 1.1)*inch, _("Billing address"))
        p.drawString(4.5*inch, (height + 0)*inch, _("Product reference"))

        global_name_client = sav_file.name_client
        if sav_file.society_client:
            global_name_client = sav_file.society_client + normal_separator + global_name_client

        p.setFont("Helvetica", 10)
        p.drawString(-0.3*inch, (height + 0.8)*inch, global_name_client)
        p.drawString(-0.3*inch, (height + 0.6)*inch, sav_file.street_client)
        p.drawString(-0.3*inch, (height + 0.4)*inch, sav_file.zipcode_client + normal_separator + sav_file.city_client)
        p.drawString(-0.3*inch, (height + 0.2)*inch, sav_file.email_client)

        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.3)*inch, _("Brand") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.3)*inch, sav_file.mark_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.5)*inch, _("Model") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.5)*inch, sav_file.name_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.7)*inch, _("Serial number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.7)*inch, sav_file.serial_number_product)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(3.7*inch, (height - 0.9)*inch, _("RMA number") + field_separator)
        p.setFont("Helvetica", 10)
        p.drawString(4.5*inch, (height - 0.9)*inch, sav_file.rma_number)

        height = 5.4

        lines = [_("VI Addr name-capital-social"), _("VI Addr street-zipcode"), _("VI Addr phone-mail"), _("VI Infos")]
        self.draw_table_one_column(-0.7, 7.6, 2, 2, _("Added informations"), lines, p)
