# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os, urllib, cStringIO

from PIL import Image
from io import BytesIO

from django.http import HttpResponse
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def some_view(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

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
    p.drawString(0.3*inch, 0.3*inch, "Hello world.")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response