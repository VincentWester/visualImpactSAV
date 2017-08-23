# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.conf import settings
from PIL import Image
from io import BytesIO
import urllib, cStringIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

from .models import SAV_file, SAV_file_status, Reparation_status, Event
from .forms import SAV_fileForm, SAV_fileUpdateForm, EventForm

def home(request):
    return render(request, 'djangoApp/home/home.html')

class SAVFileDetailView(DetailView):
    queryset = SAV_file.objects.all()
    template_name = 'djangoApp/detailSAVFile/detailSAVFile.html'

    def get_object(self):
        object = super(SAVFileDetailView, self).get_object()
        return object

    def get_context_data(self, **kwargs):
        context = super(SAVFileDetailView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')

        return context

class SAVFileCreateView(CreateView):
    model = SAV_file
    form_class = SAV_fileForm
    template_name = 'djangoApp/createSAVFile/createSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileCreateView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        print url
        print form.errors
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        form.instance.file_reference = 'VisualImpact-SAV-' + form.instance.file_reference
        return super(SAVFileCreateView, self).form_valid(form)

class SAVFileUpdateView(UpdateView):
    model = SAV_file
    form_class = SAV_fileUpdateForm
    template_name = 'djangoApp/updateSAVFile/updateSAVFile.html'

    def get_context_data(self, **kwargs):
        context = super(SAVFileUpdateView, self).get_context_data(**kwargs)
        context['current_sav_file'] = self.object
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()
        context['events'] = Event.objects.all().filter(refered_SAV_file = self.object).order_by('date')

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        return super(SAVFileUpdateView, self).form_valid(form)


DEFAULT_PAGINATION_BY = 10

class SAVFileListView(ListView):
    template_name = 'djangoApp/searchSAVFile/searchSAVFile.html'
    context_object_name = 'results'
    queryset = SAV_file.objects.all()
    paginate_by = DEFAULT_PAGINATION_BY

    def get_context_data(self, **kwargs):
        context = super(SAVFileListView, self).get_context_data(**kwargs)
        context['sav_file_status'] = SAV_file_status.objects.all()
        context['reparation_status'] = Reparation_status.objects.all()

        results = self.get_queryset()

        libelle_stats = {}
        for sav_file_status in SAV_file_status.objects.all():
            libelle_stats[sav_file_status.libelle] = results.filter(sav_file_status__libelle = sav_file_status.libelle).count()

        context['libelle_stats'] = libelle_stats
        context['nb_sav_file_status'] = results.count()
        return context

    """
    Display a SAV_file List page filtered by the search query.
    """
    def get_queryset(self):
        file_reference = self.request.GET.get('file_reference')
        tracking_number = self.request.GET.get('status')
        client_name = self.request.GET.get('client_name')
        product_name = self.request.GET.get('product_name')
        product_mark = self.request.GET.get('product_mark')
        product_serial_number = self.request.GET.get('product_serial_number')
        tracking_number = self.request.GET.get('tracking_number')
        sav_file_status = self.request.GET.get('sav_file_status')
        reparation_status = self.request.GET.get('reparation_status')
        results = SAV_file.objects.all()
        
        if file_reference:
            results = results.filter(file_reference__icontains = file_reference)

        if client_name:
            results = results.filter(name_client__icontains = client_name) 
        
        if product_name:
            results = results.filter(name_product__icontains = product_name)

        if product_mark:
            results = results.filter(mark_product__icontains = product_mark) 

        if product_serial_number:
            results = results.filter(serial_number_product__icontains = product_serial_number)

        if tracking_number:
            results = results.filter(tracking_number__icontains = tracking_number)

        if sav_file_status:
            results = results.filter(sav_file_status = sav_file_status)

        if reparation_status:
            results = results.filter(reparation_status = reparation_status)

        return results.order_by('file_reference')

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm 
    template_name = 'djangoApp/detailSAVFile/createEvent.html'

    def dispatch(self, *args, **kwargs):
        self.pkSAVFile = kwargs['pkSAVFile']

        return super(EventCreateView, self).dispatch( *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(EventCreateView, self).get_context_data(**kwargs)

        context['pkSAVFile'] = self.pkSAVFile
        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))

    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        sav_file = SAV_file.objects.get(file_reference = self.kwargs['pkSAVFile'])
        form.instance.refered_SAV_file = sav_file
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'djangoApp/detailSAVFile/updateEvent.html'

    def get_context_data(self, **kwargs):
        context = super(EventUpdateView, self).get_context_data(**kwargs)
        context['current_event'] = self.object

        return context 

    def form_invalid(self, form):
        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))
        return HttpResponse(render_to_string('djangoApp/errors/nonValideSAVFile.html', {'errors': form.errors, 'url': url}))
        
    """
    Check if the form is valid and save the object.
    """
    def form_valid(self, form):
        self.object = form.save()

        url = "{0}".format(self.request.META.get('HTTP_REFERER', '/'))

        return HttpResponseRedirect(url)

class EventDeleteView(DeleteView):
    model = Event
    template_name = 'djangoApp/detailSAVFile/confirmDeleteEvent.html'

    def get_success_url(self, *args, **kwargs): 
        return reverse_lazy('visualImpactSAV:detailSAVFile',  kwargs={ 'pk' : self.object.refered_SAV_file.file_reference }) 

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
