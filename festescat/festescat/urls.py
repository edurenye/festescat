from django.conf.urls import patterns, include, url
from ifestes.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', mainpage, name='home'),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^login/$', entra),
    url(r'^logout/$', tanca),
    url(r'^register/$', register),

    #Users
    url(r'^user/(\w+)/$', userpage),
    url(r'^user/(\w+)/edit/$', UserUpdateView.as_view(),
        name='user_edit'),

    #Organitzadors
    url(r'^user/(\w+)/org/$', org),
    url(r'^user/(\w+)/org/edit/$', OrganitzadorUpdateView.as_view(),
        name='org_edit'),

    #Festes
    url(r'^festes/$', festes, name='festes'),
    #url(r'^festes/(?P<pk>\d+)/$',
        #FestaDetail.as_view(),
        #name='festa_detail'),
    url(r'^festes/(?P<pk>\d+)/$', festa, name='festa_detail'),
    url(r'^festes/(?P<pk>\d+)/edit/$',
        LoginRequiredCheckIsOrganitzadorUpdateView.as_view(model=Festes,
            form_class=FestaForm),
        name='festa_edit'),
    url(r'^festes/(?P<pk>\d+)/assist/$', assist, name='assist'),
    url(r'^festes/(?P<pk>\d+)/no_assist/$', no_assist, name='no_assist'),
    url(r'^festes/create/$',
        LoginRequiredCheckIsOrganitzadorCreateView.as_view(model=Festes,
            form_class=FestaForm),
        name='festa_create'),
    url(r'^festes/(?P<pk>\d+)/delete/$',
        FestaDelete.as_view(), name='festa_delete'),

    #Reviews
    url(r'^festes/(?P<pk>\d+)/reviews/create/$',
        ReviewCreate.as_view(model=FestesReview, form_class=FestesReviewForm),
        name='add_review'),

    #Ubicacions
    url(r'^ubicacions/$', ubicacions, name='ubicacions'),
    url(r'^ubicacions/(?P<pk>\d+)/$',
        UbicacioDetail.as_view(),
        name='ubicacio_detail'),
    url(r'^ubicacions/(?P<pk>\d+)/edit/$',
        LoginRequiredCheckIsOrganitzadorUpdateView.as_view(model=Ubicacions,
            form_class=UbiForm),
        name='ubicacio_edit'),
    url(r'^ubicacions/create/$',
        LoginRequiredCheckIsOrganitzadorCreateView.as_view(model=Ubicacions,
            form_class=UbiForm),
        name='ubicacio_create'),
    url(r'^ubicacions/(?P<pk>\d+)/delete/$',
        UbicacioDelete.as_view(), name='ubicacio_delete'),

    #Events
    url(r'^events/$', events, name='events'),
    url(r'^events/(?P<pk>\d+)/$',
        EventDetail.as_view(),
        name='event_detail'),
    url(r'^events/(?P<pk>\d+)/edit/$',
        LoginRequiredCheckIsOrganitzadorUpdateView.as_view(model=Events,
            form_class=EventForm),
        name='event_edit'),
    url(r'^events/create/$',
        LoginRequiredCheckIsOrganitzadorCreateView.as_view(model=Events,
            form_class=EventForm),
        name='event_create'),
    url(r'^events/(?P<pk>\d+)/delete/$',
        EventDelete.as_view(), name='event_delete'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#RESTfull API
urlpatterns += patterns('',
    url(r'^api/ubicacions/$', APIUbicacionsList.as_view(), name='api_ubi-list'),
    url(r'^api/ubicacions/(?P<pk>\d+)/$', APIUbicacioDetail.as_view(),
        name='api_ubi-detail'),
    url(r'^api/events/$', APIEventsList.as_view(), name='api_event-list'),
    url(r'^api/events/(?P<pk>\d+)/$', APIEventDetail.as_view(),
        name='api_event-detail'),
    url(r'^api/festes/$', APIFestesList.as_view(), name='api_festa-list'),
    url(r'^api/festes/(?P<pk>\d+)/$', APIFestaDetail.as_view(),
        name='api_festa-detail'),
    url(r'^api/festes/(?P<pk>\d+)/review/$', APIFestaReviewsList.as_view(),
        name='api_festareviews-list'),
    url(r'^api/festes/(\d+)/review/(?P<pk>\d+)$',
        APIFestaReviewDetail.as_view(), name='api_festareview-detail'),
)

format_urlpatterns = patterns('',
    url(r'^festes\.(?P<format>[a-z0-9]+)$', festes, name='festes'),
    url(r'^festes/(?P<idFesta>\d+)\.(?P<format>[a-z0-9]+)$', festa),
    url(r'^ubicacions\.(?P<format>[a-z0-9]+)$', ubicacions,
        name='ubicacions-rest'),
    url(r'^ubicacions/(?P<idUbi>\d+)\.(?P<format>[a-z0-9]+)$', ubicacio),
    url(r'^events\.(?P<format>[a-z0-9]+)$', events, name='events-rest'),
    url(r'^events/(?P<idEvent>\d+)\.(?P<format>[a-z0-9]+)$', event),
)

urlpatterns += format_urlpatterns