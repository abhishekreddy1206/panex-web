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
from django.core.servers.basehttp import FileWrapper

import os
import tempfile
import zipfile

# Utilities #
def get_file_name(filePath):
    head, tail = os.path.split(filePath)
    return tail
# End Utilities

def send_file(request, filePath):
    """
    Send a file through Django without loading the whole file into
    memory at once. The FileWrapper will turn the file object into an
    iterator for chunks of 8KB.
    """
    filename = filePath  # Select your file here.
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    return response


def send_zipfile(request, filePath):
    """
    Create a ZIP file on disk and transmit it in chunks of 8KB,
    without loading the whole file into memory. A similar approach can
    be used for large dynamic PDF files.
    """
    temp = tempfile.TemporaryFile()
    archive = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
    filename = filePath
    archive.write(filename, get_file_name(filePath))
    # for index in range(10):
    #     filename = filePath  # Select your files here.
    #     archive.write(filename, 'file%d.txt' % index)
    archive.close()
    wrapper = FileWrapper(temp)
    response = HttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=test.zip'
    response['Content-Length'] = temp.tell()
    temp.seek(0)
    return response


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
    CONFIG = config
    existingApp = App.objects.get(pk=id)
    path_of_file = existingApp.location
    # return send_file(request, path_of_file)
    return send_zipfile(request, path_of_file)
    # response = HttpResponse(FileWrapper(myfile), content_type='application/zip')
    # response['Content-Disposition'] = 'attachment; filename=myfile.zip'
    # return response


def update(request):
    CONFIG = config
    all_apps = App.objects.all()
    return HttpResponse(serializers.serialize('json', all_apps), content_type="application/json")


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
