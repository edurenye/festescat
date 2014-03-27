# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth.models import User
#UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.core import serializers
from ifestes.models import *
from ifestes.forms import *


def mainpage(request):
    template = get_template('mainpage.html')
    variables = Context({
        'titlehead': 'Festes.cat',
        'pagetitle': 'Welcome to the Festes.cat application',
        'contentbody': 'Managing non legal funding since 2014',
        'user': request.user,
        'footer': 'Website done by Eduard Renye and Victor Diaz'
        })
    output = template.render(variables)
    return HttpResponse(output)


def userpage(request, username):
    try:
        user = Usuaris.objects.get(username=username)
        print(user)
    except:
        raise Http404('User not found.')
    events = user.assistencia.all()
    template = get_template('userpage.html')
    variables = Context({
        'username': username,
        'events': events
        })
    output = template.render(variables)
    return HttpResponse(output)


def entra(request):
    if request.method == 'POST':
        lf = LoginForm(request.POST, prefix='user')
        lf_username = request.POST['user-username']
        lf_password = request.POST['user-password']
        user = authenticate(username=lf_username, password=lf_password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                variables = Context({
                    'disabled': True,
                    'invalid': False
                    })
        else:
            variables = Context({
                'disabled': False,
                'invalid': True
                })
        return render_to_response('registration/login.html',
            dict(loginform=lf),
            context_instance=RequestContext(request, variables))
    else:
        lf = LoginForm(prefix='user')
        variables = Context({
            'disabled': False,
            'invalid': False
            })
        return render_to_response('registration/login.html',
            dict(loginform=lf),
            context_instance=RequestContext(request, variables))


def register(request):
    if request.method == 'POST':
        uf = UserForm(request.POST, prefix='user')
        if uf.is_valid():
            user_username = request.POST['user-username']
            user_password = request.POST['user-password']
            user = User.objects.create_user(user_username, user_password)
            #user = uf.models
            user.set_password(user_password)

            # = User.set_password(uf.password)
            user.save()
            return HttpResponseRedirect('/')
    else:
        uf = UserForm(prefix='user')
        return render_to_response('registration/register.html',
            dict(userform=uf),
            context_instance=RequestContext(request))


@login_required(login_url='/login')
def tanca(request):
    logout(request)
    return HttpResponseRedirect('/')


def festes(request, format='html'):
    try:
        festes = Festes.objects.all()
    except:
        raise Http404('No hi ha cap festa')
    if(format == 'html'):
        variables = Context({
            'festes': festes,
            'titlehead': 'Gestor de Festes',
            'pagetitle': 'Festes',
            })
        return render(request, "festes.html", variables)
    else:
        return formate(format, festes)


def festa(request, idFesta, format='html'):
    try:
        la_festa = Festes.objects.get(id=idFesta)
    except:
        raise Http404('No existeix aquesta festa')
    if(format == 'html'):
        events = Events.objects.filter(festa=la_festa)
        variables = Context({
            'festa': la_festa,
            'events': events,
            'titlehead': 'Detalls de la Festa',
            'pagetitle': la_festa.nom,
            })
        return render(request, "festa.html", variables)
    else:
        return formate(format, Festes.objects.filter(id=idFesta))


def ubicacions(request, format='html'):
    try:
        ubicacions = Ubicacions.objects.all()
    except:
        raise Http404('No hi ha cap ubicacio')
    if(format == 'html'):
        variables = Context({
            'ubicacions': ubicacions,
            'titlehead': "Llista dubicacions",
            'pagetitle': 'Ubicacions',
            })
        return render(request, "ubicacions.html", variables)
    else:
        return formate(format, ubicacions)


def ubicacio(request, idUbi, format='html'):
    try:
        ubicacio = Ubicacions.objects.get(id=idUbi)
    except:
        raise Http404('No existeix aquesta ubicacio')
    if(format == 'html'):
        variables = Context({
            'ubicacio': ubicacio,
            'titlehead': 'Detalls de la Ubicacio',
            'pagetitle': ubicacio.adressa,
            })
        return render(request, "ubicacio.html", variables)
    else:
        return formate(format, Ubicacions.objects.filter(id=idUbi))


def events(request, format='html'):
    try:
        events = Events.objects.all()
    except:
        raise Http404('No hi ha events')
    if(format == 'html'):
        variables = Context({
            'events': events,
            'titlehead': "Llista devents",
            'pagetitle': 'Events',
            })
        return render(request, "events.html", variables)
    else:
        return formate(format, events)


def event(request, idEvent, format='html'):
    try:
        event = Events.objects.get(id=idEvent)
    except:
        raise Http404('No existeix cap event')
    if(format == 'html'):
        variables = Context({
            'event': event,
            'titlehead': 'Detalls del event',
            'pagetitle': event.nom,
            })
        return render(request, "event.html", variables)
    else:
        return formate(format, Events.objects.filter(id=idEvent))


def formate(format, entity):
    if(format == 'json'):
        data = serializers.serialize(format, entity)
        return HttpResponse(data, mimetype='application/json')
    elif(format == 'xml'):
        data = serializers.serialize(format, entity)
        return HttpResponse(data, mimetype='application/xml')
    else:
        raise Http404('Format no valid')