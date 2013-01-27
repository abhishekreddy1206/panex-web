#!/usr/bin/python
# -*- coding: utf-8 -*-
from patient.models import Patient, Disease
from django.contrib import admin


admin.site.register(Patient)
admin.site.register(Disease)