from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView
from service.models import Service, ServiceRun


urlpatterns = patterns('',
	url(r'^new$', 'service.views.new'),
	url(r'^start/(?P<id>\d+)/$', 'service.views.start'),
	url(r'^stop/(?P<id>\d+)/$', 'service.views.stop'),
	url(r'^detail/(?P<id>\d+)/$', 'service.views.detail'),
    url(r'^$', 'service.views.index'),
)