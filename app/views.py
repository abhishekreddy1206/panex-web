#
# Copyright (c) 2013 by Mohit Singh kanwal.  All Rights Reserved.
#
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import Context, loader, RequestContext
from django import forms
from app.models import App

import os
import signal
import subprocess
import logging
import config


def index(request):
	apps = App.objects.all()
    return render(request, 'app/index.html', locals())


def handle_uploaded_file(uploadedFile):
    with open('/tmp/' + uploadedFile.name, 'wb+') as destination:
        for chunk in uploadedFile.chunks():
            destination.write(chunk)
