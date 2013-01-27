# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import simplejson
import json

def index(request):
	print "rendering index for main website"
	return render_to_response('index.html', {})

def show_json(request):
	response_data = dict()
	response_data['result'] = 'failed'
	response_data['message'] = 'you messed up'
	return HttpResponse(json.dumps(response_data), content_type="application/json")