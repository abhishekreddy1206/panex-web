# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404, render
from service.models import Service, ServiceRun
from django.template import Context, loader, RequestContext
from django import forms
from service.forms import ServiceForm, ServiceStartForm 
from django.contrib import messages

import os
import signal
import subprocess
import logging

def index(request):
    all_services = Service.objects.all()

    print "within index All services ", all_services.count()
    running_services = ServiceRun.objects.all().filter(status="RUNNING")
    # Check each running_service and update
    for aRunningService in running_services:
        if pid_running(aRunningService.pid):
            aRunningService.status = "STOPPED"
            aRunningService.pid = -1 # Reset PID
            aRunningService.save()
    running_services = ServiceRun.objects.all().filter(status="RUNNING")
    print "Running Services count ", running_services.count()
    return render(request, 'service/index.html', locals())

def pid_running(pid):        
    """ Check For the existence of a unix pid. """
    try:
        os.kill(pid, 0)
        # Signal zero is not killing of the process
        # Just asking whether u are running or not
    except OSError:
        return True
    else:
        return False

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
            location = '/tmp/' + request.FILES['file'].name

            aService = Service(name=name, description=desc, command=command, location=location)
            aService.save()
            # Run the service in the background
            messages.add_message(request, messages.SUCCESS, 'Successfully Created')
            return HttpResponseRedirect('/service/')
    else:
        form = ServiceForm()
    return render(request, 'service/new.html', {'form': form})


def handle_uploaded_file(uploadedFile):
    with open('/tmp/' + uploadedFile.name, 'wb+') as destination:
        for chunk in uploadedFile.chunks():
            destination.write(chunk)

def start(request,id):
    """Starts a service running in the background"""
    if request.method == 'POST':
        form = ServiceStartForm(request.POST)
        if form.is_valid():
            print "Handling a valid form"
            service_id = form.cleaned_data['serviceChoice']
            input_dir = form.cleaned_data['input_directory']
            output_dir = form.cleaned_data['output_directory']

            aEntry = Service.objects.get(pk=service_id)
            aServiceRun = ServiceRun(service=aEntry, inputParams=input_dir, outputParams=output_dir)
            aServiceRun.save()

            # elevate permissions in order to run
            subprocess.call(["chmod", "a+x", aServiceRun.service.location])

            process = subprocess.Popen(aServiceRun.service.location, shell=False)
            # process = subprocess.Popen("mvim", shell=False)
            # process = subprocess.Popen("mvim", shell=False, preexec_fn=os.setpgrp) #preexec_fn=os.setpgrp
            print 'process id of service is: %s', process.pid
            aServiceRun.status="RUNNING"
            aServiceRun.pid = process.pid
            aServiceRun.save()
            messages.add_message(request, messages.SUCCESS, 'Successfully Started')
            return HttpResponseRedirect('/service/')
    else:
        form = ServiceStartForm()
        print "Invalid form, not a POST request"
    return render(request, 'service/start.html', locals())

def stop(request, id):
    """Stops a service"""
    runningService = ServiceRun.objects.get(pk=id)
    ret = subprocess.call(["kill", "-9", "%d" % runningService.pid])
    # ret = os.killpg(runningService.pid, signal.SIGTERM)
     
    if ret == 0:
        runningService.pid = -1
        runningService.status = "STOPPED"
        runningService.save()
        messages.add_message(request, messages.SUCCESS, 'Service Successfully Stopped')
    else:
        messages.add_message(request, messages.ERROR, 'Cant stop the service check the logs')
    all_services = Service.objects.all()
    running_services = ServiceRun.objects.all().filter(status="RUNNING")
    return render(request, 'service/index.html', locals())
