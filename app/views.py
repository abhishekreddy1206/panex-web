#
# Copyright (c) 2013 by Mohit Singh kanwal.  All Rights Reserved.
#
import json
import os
from app.forms import AppForm
from app.models import App
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from panex_web import config
from django.contrib import messages

def index(request):
    apps = App.objects.all()
    return render(request, 'app/index.html', locals())


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def handle_uploaded_file(uploadedFile):
    CONFIG = config
    # Ensure that APP_DIR exists
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

def delete(request, id):
    CONFIG = config
    existingApp = App.objects.get(pk=id)
    existingApp.delete()
    messages.add_message(request, messages.SUCCESS, 'Successfully Deleted')
    return HttpResponseRedirect('/app/')

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

            messages.add_message(request, messages.SUCCESS, 'Successfully Created')
            return HttpResponseRedirect('/app/')
    else:
        form = AppForm()
    return render(request, 'app/new.html', locals())
