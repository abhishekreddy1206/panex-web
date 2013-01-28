# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from service.models import Service, ServiceRun
from django.template import Context, loader, RequestContext
from django import forms
from service.forms import ServiceForm, DivErrorList

import os


def index(request):
	print "[service] Rendering Index Page"
	return render_to_response('service/index.html', {})


def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def new(request):
    # Restrict To within SoC
    print ip_address_processor(request)['ip_address']

    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            name = form.cleaned_data['name']
            desc = form.cleaned_data['description']
            command = form.cleaned_data['command']
            location = '/tmp/'+request.FILES['file'].name

            aService = Service(name=name, description=desc, command=command, location=location)
            aService.save()
            return HttpResponseRedirect('/service/')
    else:
        form = ServiceForm()
    return render(request, 'service/new.html', {'form': form})

def handle_uploaded_file(uploadedFile):
    with open('/tmp/'+uploadedFile.name, 'wb+') as destination:
        for chunk in uploadedFile.chunks():
            destination.write(chunk)
