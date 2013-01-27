# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from service.models import Service, ServiceRun
from django.template import Context, loader, RequestContext


def index(request):
	print "[service] Rendering Index Page"
	return render_to_response('service/index.html', {})

def ip_address_processor(request):
    return {'ip_address': request.META['REMOTE_ADDR']}
