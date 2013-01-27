from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from service.models import Service, ServiceRun


urlpatterns = patterns('',
    url(r'^home$', 'service.views.index'),
)