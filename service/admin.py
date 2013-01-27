#!/usr/bin/python
# -*- coding: utf-8 -*-
from service.models import Service, ServiceRun
from django.contrib import admin


admin.site.register(Service, ServiceRun)
