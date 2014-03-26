# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response
from django.forms import *
from ifestes.models import *


def mainpage(request):
    template = get_template('mainpage.html')
    variables = Context({
        'titlehead': 'Festes.cat',
        'pagetitle': 'Welcome to the Festes.cat application',
        'contentbody': 'Managing non legal funding since 2014',
        'user': request.user,
        'footer': 'Webside done by Eduard Renye and Victor Diaz'
        })
    output = template.render(variables)
    return HttpResponse(output)


def userpage(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        raise Http404('User not found.')
    festes = user.sobre_set.all()
    template = get_template('userpage.html')
    variables = Context({
        'username': username,
        'festes': festes
        })
    output = template.render(variables)
    return HttpResponse(output)


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            uf.save()
            return HttpResponseRedirect('/')
    else:
        uf = UserForm(prefix='user')
        return render_to_response('register.html',
            dict(userform=uf),
            context_instance=RequestContext(request))


def festes(request):
    try:
        festes = Festes.objects.all()
    except:
        raise Http404('Festes not found')
    variables = Context({
        'festes': festes,
        'titlehead': 'Gestor de Festes',
        'pagetitle': 'Festes',
        })
    return render(request, "festes.html", variables)


def festa(request, idFestes):
    try:
        festa = Festes.object.get(pk=idFestes)
    except:
        raise Http404('Festa not found')
    variables = Context({
        'festa': idFestes,
        'titlehead': 'Detalls de la Festa',
        'pagetitle': festa.nom,
        })
    return render(request, "festa.html", variables)