from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
	url(r'^new$','patient.views.new'),
	url(r'^$', 'patient.views.index'),
)