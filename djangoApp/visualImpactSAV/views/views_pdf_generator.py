# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, urllib, cStringIO

from PIL import Image
from io import BytesIO

from django.http import HttpResponse
from django.conf import settings
from django.views.generic.edit import CreateView
from django.shortcuts import get_object_or_404

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# models part
from visualImpactSAV.models import Pdf_client_invoice_file, Designation, SAV_file
# forms part
from visualImpactSAV.forms import Pdf_client_invoice_file_form

class PDFGeneratorCreateView(CreateView):
    model = Pdf_client_invoice_file
    form_class = Pdf_client_invoice_file_form
    template_name = 'djangoApp/pdfGenerator/createOrUpdatePdf.html'

    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']

        return super(PDFGeneratorCreateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PDFGeneratorCreateView, self).get_context_data(**kwargs)

        context['pkSAVFile'] = self.pkSAVFile
        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = get_object_or_404(SAV_file, file_reference=self.pkSAVFile)
        form.instance.refered_sav_file = sav_file
        return self.generate_pdf(form)
        #return super(PDFGeneratorUpdateView, self).form_valid(form)

    def generate_pdf(self, form):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="{0}"'.format(form.instance.filename)

        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(buffer)
        p.translate(inch,inch)

        url = os.path.join(settings.STATICFILES_DIRS[0], 'images/logoVisual.jpg')

        file = cStringIO.StringIO(urllib.urlopen(url).read())
        img = Image.open(file)

        p.drawInlineImage(img, -0.7*inch, 10*inch, 122, 39)
        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(0.3*inch, 0.3*inch, form.instance.filename)
        p.drawString(0.7*inch, 0.7*inch, form.instance.refered_sav_file.name_client)

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response