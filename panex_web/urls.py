from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'panex_web.views.home', name='home'),
    # url(r'^panex_web/', include('panex_web.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^show_json', 'panex_web.views.show_json'),
    url(r'^$', 'panex_web.views.index'),
    url(r'^service/', include('service.urls')),
    url(r'^app/', include('app.urls')),
    url(r'^patient/', include('patient.urls')),
)
