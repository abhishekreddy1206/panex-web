from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
	# JSON
	url(r'^update/$', 'app.views.update'),
	# HTML
	url(r'^new/$', 'app.views.new'),
	url(r'^$', 'app.views.index'),
)