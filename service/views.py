# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from service.models import Service, ServiceRun
from django.template import Context, loader, RequestContext


def index(request):
	return render_to_response('index.html', {},
                              RequestContext(request))
