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

import constants
from visualImpactSAV.models import SAV_file


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
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_TITLE_SIZE)
        p.drawString(3*inch, 10.2*inch, self.title)

    def build_pdf(self, p):
        template = self.build_template()

        for part in template:
            draw_next_part = getattr(self, part['func'])
            draw_next_part(p=p, **part['kwargs'])

    def draw_raw_text(self, p, alinea, height_start, lines):
        p.setFont(constants.FONT_STYLE, constants.FONT_NORMAL_SIZE)
        height = height_start
        for line in lines:
            p.drawString(alinea*inch, height*inch, line)
            height -= 0.2

    def draw_raw_text_with_bold(self, p, lines):
        for line in lines:
            p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
            p.drawString(line[1]*inch, line[0]*inch, line[2])
            p.setFont(constants.FONT_STYLE, constants.FONT_NORMAL_SIZE)
            p.drawString(line[3]*inch, line[0]*inch, line[4])

    def draw_title_and_text_in_column(self, p, alinea, height_start, alinea_title, title, lines):
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
        p.drawString(alinea_title*inch, height_start*inch, title)

        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
        height = height_start - 0.3
        for line in lines:
            p.drawString(alinea*inch, height*inch, line)
            height -= 0.2

    def draw_title_and_text_tuple_in_column(self, p, alinea, height_start, alinea_title, title, lines):
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
        p.drawString(alinea_title*inch, height_start*inch, title)

        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
        height = height_start - 0.3
        for line in lines:
            p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
            p.drawString(line[0]*inch, height*inch, line[1])
            p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
            p.drawString(line[2]*inch, height*inch, line[3])
            height -= 0.2

    def draw_table_one_column(self, p, alinea, height, length, alinea_title, alinea_lines, title, lines):
        height_column = len(lines) * 0.2
        p.rect(alinea*inch, height*inch, length*inch, (height_column + 0.5)*inch, fill=0)
        p.line(alinea*inch, (height + 1)*inch, (length - 0.5)*inch, (height + 1)*inch)
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
        p.drawString(alinea_title*inch, (height + 1.1)*inch, title)
        p.setFont(constants.FONT_STYLE, constants.FONT_SMALL_SIZE)

        for line in lines:
            p.drawString(alinea_lines*inch, (height + height_column)*inch, line)
            height_column -= 0.2

    def draw_table_several_columns(self, p, alinea_start, bottom_start,
                                   length_table, height_table, height_title_line,
                                   alinea_title, height_title, title, lines):
        p.rect(alinea_start*inch, bottom_start*inch, length_table*inch, height_table*inch, fill=0)

        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
        p.drawString(alinea_title*inch, height_title*inch, title)

        height_line = bottom_start + height_table - height_title_line
        end_line = alinea_start + length_table
        p.line(alinea_start*inch, height_line*inch, end_line*inch, height_line*inch)

        for line in lines:
            p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
            p.drawString(line[0]*inch, (height_line-0.2)*inch, line[1])
            p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
            p.drawString(line[0]*inch, (height_line-0.4)*inch, line[2])

    def draw_description_part(self, p, alinea_title, alinea_text, height):
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_NORMAL_SIZE)
        p.drawString(alinea_title*inch, (height)*inch, _("Problems' description"))
        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)


        # this trick is used for deleting the EOF character
        lines = self.sav_file.out_of_order_reason.split('\n')
        size = len(lines)
        for i in range(size):
            height = height - 0.3
            line = lines[i] if i == size - 1 else lines[i][:-1]
            p.drawString(alinea_text*inch, height*inch, line)

    def draw_designations_part(self, p, height_start, lines):
        height = height_start
        p.drawString(0*inch, height*inch, _("Designations"))
        p.drawString(4.8*inch, height*inch, _("Quantity"))
        p.drawString(5.8*inch, height*inch, _("Pre-tax price"))
        p.line(-0.5*inch, (height - 0.1)*inch, 6.7*inch, 5.4*inch)
        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)

        total = Decimal(0.0)
        height = height - 0.3

        for i, designation in enumerate(lines):
            height = height - 0.2
            p.drawString(-0.3*inch, height*inch, str(i + 1) + constants.NORMAL_SEPARATOR)
            p.drawString(0*inch, height*inch, designation.designation)
            p.drawString(4.8*inch, height*inch, str(designation.quantity))
            p.drawString(5.8*inch, height*inch, str(designation.price) + _(" £"))
            total += Decimal(designation.quantity) * Decimal(designation.price)

        height = height - 0.2
        p.line(4.5*inch, height*inch, 6.7*inch, height*inch)
        height = height - 0.2

        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
        p.drawString(-0.3*inch, height*inch, _("All our prices are given as excluding tax"))
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
        p.drawString(4.5*inch, height*inch, _("Total pre-tax price") + constants.FIELD_SEPARATOR)
        p.drawString(5.8*inch, height*inch, str(round(total, 2)).encode('utf8') + _(" £"))
        height = height - 0.2
        p.setFont(constants.FONT_STYLE, constants.FONT_SMALLER_SIZE)
        p.drawString(-0.3*inch, height*inch, _("Transport fees when asked except where otherwise specified"))
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
        p.drawString(4.5*inch, height*inch, ("Tax") + constants.FIELD_SEPARATOR)
        p.drawString(5.8*inch, height*inch, _("Tax percent"))
        height = height - 0.125
        p.setFont(constants.FONT_STYLE, constants.FONT_VERY_SMALL_SIZE)
        p.drawString(-0.3*inch, height*inch, _("Buying condition 1"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 2"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 3"))
        height = height - 0.075
        p.drawString(-0.3*inch, height*inch, _("Buying condition 4"))
        height = height - 0.025
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
        p.drawString(4.5*inch, height*inch, _("Total price AI") + constants.FIELD_SEPARATOR)
        p.setFillColorRGB(1, 0, 0)
        p.drawString(5.8*inch, height*inch, str(round(total * Decimal(1.2), 2)).encode('utf8') + _(" £"))
        p.setFillColorRGB(0, 0, 0)
        height = height - 0.05
        p.rect(-0.5*inch, height*inch, 4.7*inch, 0.835*inch, fill=0)

        p.setFillColorRGB(1, 0, 0)
        height = height - 0.25
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALLER_SIZE)
        p.drawString(-0.3*inch, height*inch, _("ALL REFUSED COST ESTIMATE WILL BE FACTURED 90£ (TAX EXCLUDED)"))
        height = height - 0.1
        p.rect(-0.5*inch, height*inch, 7.2*inch, 0.3*inch, fill=0)
        height = height - 0.225

        p.setFillColorRGB(0, 0, 0)
        p.setFont(constants.FONT_STYLE_BOLD, constants.FONT_SMALL_SIZE)
        p.drawString(-0.3*inch, height*inch, _("Delivery time") + constants.FIELD_SEPARATOR)
        p.drawString(3.3*inch, height*inch, _("Means of payment") + constants.FIELD_SEPARATOR)
        p.setFont(constants.FONT_STYLE, constants.FONT_SMALL_SIZE)
        p.drawString(0.9*inch, height*inch, _("to confirm"))
        p.drawString(4.5*inch, height*inch, _("to define before the command"))
        height = height - 0.125
        p.rect(-0.5*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)
        p.rect(3.1*inch, height*inch, 3.6*inch, 0.3*inch, fill=0)


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
        super(Pdf_generator_client, self).__init__(_("customer-summary"), _("Summary after sell sheet"))

    def build_template(self):
        sav_file = self.sav_file
        global_name_client = sav_file.name_client
        if sav_file.society_client:
            global_name_client = sav_file.society_client + constants.NORMAL_SEPARATOR + global_name_client

        template = [
            {
                'func': "draw_raw_text_with_bold",
                'kwargs': {
                    'lines': [
                        (9.5, -0.5, _("Reference") + constants.FIELD_SEPARATOR, 0.5, _("VIF-AS-") + str(sav_file.id)),
                        (9.5, 3.2, _("Creation date") + constants.FIELD_SEPARATOR, 5, sav_file.creation_date.strftime("%d/%m/%Y %H:%M")),
                        (9.2, -0.5, _("Managed by") + constants.FIELD_SEPARATOR, 0.5, sav_file.registred_by.username),
                        (9.2, 3.2, _("Customer name") + constants.FIELD_SEPARATOR, 5, global_name_client),
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height_start': 8.7,
                    'alinea_title': -0.5,
                    'title': _("Billing address"),
                    'lines': [
                        global_name_client,
                        sav_file.street_client,
                        sav_file.zipcode_client + constants.NORMAL_SEPARATOR + sav_file.city_client,
                        sav_file.email_client
                    ]
                }
            },
            {
                'func': "draw_title_and_text_tuple_in_column",
                'kwargs': {
                    'alinea': 4.5,
                    'height_start': 7.6,
                    'alinea_title': 4.5,
                    'title': _("Product reference"),
                    'lines': [
                        (
                            3.7,
                            _("Brand") + constants.FIELD_SEPARATOR,
                            5,
                            sav_file.mark_product,
                        ),
                        (
                            3.7,
                            _("Model") + constants.FIELD_SEPARATOR,
                            5,
                            sav_file.name_product,
                        ),
                        (
                            3.7,
                            _("Serial number") + constants.FIELD_SEPARATOR,
                            5,
                            sav_file.serial_number_product,
                        ),
                        (
                            3.7,
                            _("RMA number") + constants.FIELD_SEPARATOR,
                            5,
                            sav_file.rma_number if sav_file.rma_number else  _("Unknown"),
                        )
                    ]
                }
            },
            {
                'func': "draw_description_part",
                'kwargs': {
                    'alinea_title': 2.2,
                    'alinea_text': -0.3,
                    'height': 6,
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': 0.8,
                    'length': 7.6,
                    'alinea_title': 2,
                    'alinea_lines': -0.4,
                    'title': _("Conditions"),
                    'lines': [
                        _("VI Addr name-capital-social"),
                        _("VI Addr street-zipcode"),
                        _("VI Addr phone-mail"),
                        _("VI Infos")
                    ]
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': -0.7,
                    'length': 7.6,
                    'alinea_title': 2,
                    'alinea_lines': 2,
                    'title': _("Added informations"),
                    'lines': [
                        _("VI Addr name-capital-social"),
                        _("VI Addr street-zipcode"),
                        _("VI Addr phone-mail"),
                        _("VI Infos")
                    ]
                }
            },
        ]
        return template


class Pdf_generator_cost_estimate(Pdf_generator):
    def __init__(self):
        super(Pdf_generator_cost_estimate, self).__init__(_("cost-estimate"), _("Commercial offer"))

    def build_template(self):
        sav_file = self.sav_file
        designations = sav_file.designations.all()
        global_name_client = sav_file.name_client
        if sav_file.society_client:
            global_name_client = sav_file.society_client + constants.NORMAL_SEPARATOR + global_name_client

        height_start_designations_part = 5.5
        height_taken_by_designations = designations.count() * 0.2
        # 3.075 is the result of the sum of all the height taken by the other parts of this pdf
        # excluding the designation list height, in the method `draw_designations_part`
        heigh_start_for_bank_info = height_start_designations_part - 3.4 - designations.count() * 0.2
        heigh_start_for_VI_info = heigh_start_for_bank_info - 1.35

        template = [
            {
                'func': "draw_raw_text",
                'kwargs': {
                    'alinea': -0.5,
                    'height_start': 9.6,
                    'lines': [
                        _("AS file reference") + constants.FIELD_SEPARATOR + _("VIF-AS-") + str(sav_file.id),
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height_start': 9.2,
                    'alinea_title': -0.5,
                    'title': _("Billing address"),
                    'lines': [
                        global_name_client,
                        sav_file.street_client,
                        sav_file.zipcode_client + constants.NORMAL_SEPARATOR + sav_file.city_client,
                        sav_file.email_client
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': 4,
                    'height_start': 7.8,
                    'alinea_title': 4,
                    'title': _("File managed by") + constants.FIELD_SEPARATOR + sav_file.registred_by.username,
                    'lines': [
                        _("VI Addr name"),
                        _("VI Addr street"),
                        _("VI Addr zipcode"),
                        sav_file.registred_by.email
                    ]
                }
            },
            {
                'func': "draw_table_several_columns",
                'kwargs': {
                    'alinea_start': -0.5,
                    'bottom_start': 5.9,
                    'length_table': 7.2,
                    'height_table': 0.8,
                    'height_title_line': 0.3,
                    'alinea_title': 2.1,
                    'height_title': 6.5,
                    'title': _("Product reference"),
                    'lines': [
                        (
                            -0.3,
                            _("Brand") + constants.FIELD_SEPARATOR,
                            sav_file.mark_product,
                        ),
                        (
                            1.5,
                            _("Model") + constants.FIELD_SEPARATOR,
                            sav_file.name_product,
                        ),
                        (
                            3.7,
                            _("Serial number") + constants.FIELD_SEPARATOR,
                            sav_file.serial_number_product,
                        ),
                        (
                            5.5,
                            _("RMA number") + constants.FIELD_SEPARATOR,
                            sav_file.rma_number if sav_file.rma_number else _("Unknown"),
                        )
                    ]
                }
            },
            {
                'func': "draw_designations_part",
                'kwargs': {
                    'height_start': height_start_designations_part,
                    'lines': designations
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': heigh_start_for_bank_info,
                    'length': 7.2,
                    'alinea_title': 2,
                    'alinea_lines': 2,
                    'title': _("Bank details"),
                    'lines': [
                        _("VI Addr name-capital-social"),
                        _("VI Addr street-zipcode"),
                        _("VI Addr phone-mail"),
                        _("VI Infos")
                    ]
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': heigh_start_for_VI_info,
                    'length': 7.2,
                    'alinea_title': 2,
                    'alinea_lines': 2,
                    'title': _("Added informations"),
                    'lines': [
                        _("VI bank-code bank"),
                        _("VI RIB"),
                        _("VI IBAN"),
                        _("VI account owner")
                    ]
                }
            },
        ]
        return template


class Pdf_generator_furnisher(Pdf_generator):
    def __init__(self):
        super(Pdf_generator_furnisher, self).__init__(_("repairs"), _("Repairs asking"))

    def build_template(self):
        sav_file = self.sav_file
        furnisher = sav_file.furnisher
        template = [
            {
                'func': "draw_raw_text",
                'kwargs': {
                    'alinea': -0.5,
                    'height_start': 9.6,
                    'lines': [
                        _("AS file reference") + constants.FIELD_SEPARATOR + _("VIF-AS-") + str(sav_file.id),
                        _("Please, tell this reference number in all our correspondances.")
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height_start': 8.7,
                    'alinea_title': -0.5,
                    'title': _("Furnisher address"),
                    'lines': [
                        furnisher.mark,
                        furnisher.street + constants.COMA_SEPARATOR + furnisher.complements,
                        furnisher.zipcode + constants.FIELD_SEPARATOR + furnisher.city,
                        furnisher.phone
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': 4,
                    'height_start': 7.5,
                    'alinea_title': 4,
                    'title': _("File managed by") + constants.FIELD_SEPARATOR + sav_file.registred_by.username,
                    'lines': [
                        _("VI Addr name"),
                        _("VI Addr street"),
                        _("VI Addr zipcode"),
                        sav_file.registred_by.email
                    ]
                }
            },
            {
                'func': "draw_table_several_columns",
                'kwargs': {
                    'alinea_start': -0.5,
                    'bottom_start': 5.8,
                    'length_table': 7.2,
                    'height_table': 0.8,
                    'height_title_line': 0.3,
                    'alinea_title': 2.1,
                    'height_title': 6.4,
                    'title': _("Product reference"),
                    'lines': [
                        (
                            -0.3,
                            _("Brand") + constants.FIELD_SEPARATOR,
                            sav_file.mark_product,
                        ),
                        (
                            1.5,
                            _("Model") + constants.FIELD_SEPARATOR,
                            sav_file.name_product,
                        ),
                        (
                            3.7,
                            _("Serial number") + constants.FIELD_SEPARATOR,
                            sav_file.serial_number_product,
                        ),
                        (
                            5.5,
                            _("RMA number") + constants.FIELD_SEPARATOR,
                            sav_file.rma_number if sav_file.rma_number else _("Unknown"),
                        )
                    ]
                }
            },
            {
                'func': "draw_description_part",
                'kwargs': {
                    'alinea_title': 2.5,
                    'alinea_text': -0.3,
                    'height': 5.4,
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': -0.7,
                    'length': 7.6,
                    'alinea_title': 2,
                    'alinea_lines': 2,
                    'title': _("Added informations"),
                    'lines': [
                        _("VI Addr name-capital-social"),
                        _("VI Addr street-zipcode"),
                        _("VI Addr phone-mail"),
                        _("VI Infos")
                    ]
                }
            },
        ]
        return template


class Pdf_answer_reparation(Pdf_generator):
    def __init__(self):
        super(Pdf_answer_reparation, self).__init__(_("repairs-return"), _("Repairs return"))

    def build_template(self):
        sav_file = self.sav_file
        global_name_client = sav_file.name_client
        if sav_file.society_client:
            global_name_client = sav_file.society_client + constants.NORMAL_SEPARATOR + global_name_client

        template = [
            {
                'func': "draw_raw_text_with_bold",
                'kwargs': {
                    'lines': [
                        (9.5, -0.5, _("Reference") + constants.FIELD_SEPARATOR, 0.8, _("VIF-AS-") + str(sav_file.id)),
                        (9.5, 3.7, _("Managed by") + constants.FIELD_SEPARATOR, 5, sav_file.registred_by.username),
                        (9.2, -0.5, _("Customer name") + constants.FIELD_SEPARATOR, 0.8, global_name_client),
                    ]
                }
            },
            {
                'func': "draw_title_and_text_in_column",
                'kwargs': {
                    'alinea': 2.3,
                    'height_start': 8.7,
                    'alinea_title': 2,
                    'title': _("Billing address"),
                    'lines': [
                        global_name_client,
                        sav_file.street_client,
                        sav_file.zipcode_client + constants.NORMAL_SEPARATOR + sav_file.city_client,
                        sav_file.email_client
                    ]
                }
            },
            {
                'func': "draw_table_several_columns",
                'kwargs': {
                    'alinea_start': -0.5,
                    'bottom_start': 6.5,
                    'length_table': 7.2,
                    'height_table': 0.8,
                    'height_title_line': 0.3,
                    'alinea_title': 2.1,
                    'height_title': 7.1,
                    'title': _("Product reference"),
                    'lines': [
                        (
                            -0.3,
                            _("Brand") + constants.FIELD_SEPARATOR,
                            sav_file.mark_product,
                        ),
                        (
                            1.5,
                            _("Model") + constants.FIELD_SEPARATOR,
                            sav_file.name_product,
                        ),
                        (
                            3.3,
                            _("Serial number") + constants.FIELD_SEPARATOR,
                            sav_file.serial_number_product,
                        ),
                        (
                            5.2,
                            _("RMA number") + constants.FIELD_SEPARATOR,
                            sav_file.rma_number if sav_file.rma_number else  _("Unknown"),
                        )
                    ]
                }
            },
            {
                'func': "draw_table_one_column",
                'kwargs': {
                    'alinea': -0.5,
                    'height': -0.7,
                    'length': 7.6,
                    'alinea_title': 2,
                    'alinea_lines': 2,
                    'title': _("Added informations"),
                    'lines': [
                        _("VI Addr name-capital-social"),
                        _("VI Addr street-zipcode"),
                        _("VI Addr phone-mail"),
                        _("VI Infos")
                    ]
                }
            },
        ]
        return template