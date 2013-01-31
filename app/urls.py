from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
	# JSON
	url(r'^update/$', 'app.views.update'),
	url(r'^download/(?P<id>\d+)/$', 'app.views.download'),
	# HTML
	url(r'^new/$', 'app.views.new'),
	url(r'^$', 'app.views.index'),
)