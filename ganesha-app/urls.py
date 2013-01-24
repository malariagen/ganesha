from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from ganesha.api import v1_api

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ganesha.views.home', name='home'),
    # url(r'^ganesha/', include('ganesha.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^htsql/', include('htsql_django.urls')),

    (r'^api/', include(v1_api.urls)),
)
