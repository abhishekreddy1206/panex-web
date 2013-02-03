from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from panex_web import config
from django.contrib import messages
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from patient.models import Patient, Disease
import json

def index(request):
	CONFIG = config
	all_patients = Patient.objects.all()
	return HttpResponse(serializers.serialize('json', all_patients), content_type="application/json")

# @csrf_protect
# needed to ensure that JSON post requests work
@csrf_exempt
def new(request):
	if request.method == 'POST':
		json_data = simplejson.loads(request.raw_post_data)
		try:
			patient = dict(json_data['patient'])
		except KeyError:
			return HttpResponseServerError("Malformed Data")
		return HttpResponse(json.dumps(patient), content_type="application/json", status=200)

	else:
		return HttpResponse("Only JSON post accepted", status=404)

