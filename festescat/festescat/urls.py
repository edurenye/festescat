from django.conf.urls import patterns, include, url
from rest_framework.urlpatterns import format_suffix_patterns
from ifestes.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', mainpage, name='home'),
    url(r'^user/(\w+)/$', userpage),
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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

format_urlpatterns = patterns('',
    url(r'^festes$', festes, name='festes'),
    url(r'^festes/(?P<idFesta>\d+)$', festa),
    url(r'^ubicacions$', ubicacions, name='ubicacions'),
    url(r'^ubicacions/(?P<idUbi>\d+)$', ubicacio),
    url(r'^events$', events, name='events'),
    url(r'^events/(?P<idEvent>\d+)$', event),
)

format_urlpatterns = format_suffix_patterns(format_urlpatterns)

urlpatterns += format_urlpatterns