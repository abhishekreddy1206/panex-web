#
# Copyright (c) 2013 by Mohit Singh kanwal.  All Rights Reserved.
#
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core import serializers
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from django import forms
from app.models import App
from app.forms import AppForm
from panex_web import config

import os
import signal
import subprocess
import logging
import json


def index(request):
    apps = App.objects.all()
    return render(request, 'app/index.html', locals())


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def handle_uploaded_file(uploadedFile):
    CONFIG = config
    ensure_dir(CONFIG.APP_DIRECTORY)
    with open(CONFIG.APP_DIRECTORY + uploadedFile.name, 'wb+') as destination:
        for chunk in uploadedFile.chunks():
            destination.write(chunk)

def download(request, id):
    ## TODO: add proper streaming of bits of the correct software
    response_data = dict()
    response_data['result'] = 'failed'
    response_data['message'] = 'you messed up'
    return HttpResponse(json.dumps(response_data), content_type="application/json")

def update(request):
    CONFIG = config
    all_apps = App.objects.all()
    return HttpResponse(serializers.serialize('json',all_apps), content_type="application/json")


def new(request):
    CONFIG = config
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            name = form.cleaned_data['name']
            desc = form.cleaned_data['description']
            author = form.cleaned_data['author']
            version = form.cleaned_data['version']
            location = CONFIG.APP_DIRECTORY + request.FILES['file'].name
            anApp = App(name=name, description=desc, version=version, location=location, author=author)
            anApp.save()

            error_message = "Successfully Created."
            return HttpResponseRedirect('/app/')
    else:
        form = AppForm()
    return render(request, 'app/new.html', locals())
