# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from service.models import Service, ServiceRun
from django.template import Context, loader, RequestContext
from django import forms
from service.forms import ServiceForm

def index(request):
	print "[service] Rendering Index Page"
	return render_to_response('service/index.html', {})


def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}


def new(request):
	form = ServiceForm(request.POST)
	if request.method == 'POST':
		if form.is_valid():
			return HttpResponseRedirect('/thanks/')
	else:
		form = ServiceForm()
	return render(request, 'service/new.html', {
        'form': form,
    })
