from django.conf.urls import patterns, include, url
from django.views.generic import UpdateView
from ifestes.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', mainpage, name='home'),
    url(r'^user/(\w+)/$', userpage),
    url(r'^user/(\w+)/org/$', org),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', entra),
    url(r'^logout/$', tanca),
    url(r'^register/$', register),
    url(r'^festes/$', festes, name='festes'),
    url(r'^festes/(\d+)/$', festa),
    url(r'^ubicacions/$', ubicacions, name='ubicacions'),
    url(r'^ubicacions/(\d+)/$', ubicacio),
    url(r'^events/$', events, name='events'),
    url(r'^events/(\d+)/$', event),

    url(r'^ubicacions/(\d+)/edit/$', APIUbicacioDetail.as_view(),name='ubi-detail'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

format_urlpatterns = patterns('',
    url(r'^festes\.(?P<format>[a-z0-9]+)$', festes, name='festes'),
    url(r'^festes/(?P<idFesta>\d+)\.(?P<format>[a-z0-9]+)$', festa),
    url(r'^ubicacions\.(?P<format>[a-z0-9]+)$', ubicacions, name='ubicacions'),
    url(r'^ubicacions/(?P<idUbi>\d+)\.(?P<format>[a-z0-9]+)$', ubicacio),
    url(r'^events\.(?P<format>[a-z0-9]+)$', events, name='events'),
    url(r'^events/(?P<idEvent>\d+)\.(?P<format>[a-z0-9]+)$', event),
)

urlpatterns += format_urlpatterns