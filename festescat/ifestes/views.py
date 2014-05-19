# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import Context, RequestContext
from django.template.loader import get_template
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
    if request.method == 'POST':
        user = request.user
        uf = UserFormEdit(request.POST, prefix='user', instance=user)
        if uf.is_valid():
            user_password = request.POST['user-password']
            user.set_password(user_password)
            user.save()
            return HttpResponseRedirect('/')
    else:
        uf = UserFormEdit(prefix='user')
        try:
            user = Usuaris.objects.get(username=username)
            print(user)
        except:
            raise Http404('User not found.')
        events = user.assistencia.all()
        variables = Context({
            'user': request.user,
            'username': username,
            'events': events
            })
        return render_to_response('userpage.html',
            dict(userform=uf),
            context_instance=RequestContext(request, variables))


def org(request, username):
    if request.method == 'POST':
        of = OrgForm(request.POST, prefix='org')
        user = Usuaris.objects.get(username=username)
        empresa = request.POST['org-empresa']
        org = Organitzadors(usuaris_ptr=user, username=user.username, password=user.password, empresa=empresa)
        org.save()
        return HttpResponseRedirect('/')
    else:
        variables = Context({
            'user': request.user,
            'username': username,
            })
        of = OrgForm(prefix='org')
        return render_to_response('org.html',
            dict(orgform=of),
            context_instance=RequestContext(request, variables))


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
            user_email = request.POST['user-email']
            user_password = request.POST['user-password']
            user = Usuaris.objects.create_user(user_username, user_email,
                user_password)
            #user = uf.models
            user.set_password(user_password)
            user.save()
            user = authenticate(username=user_username, password=user_password)
            login(request, user)
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
    if request.method == 'POST':
        nff = NewFestaForm(request.POST)
        user = request.user
        org = Organitzadors.objects.get(username=user.username)
        f_nom = request.POST['nom']
        f_data_inici = request.POST['data_inici']
        f_data_fi = request.POST['data_fi']
        f_categoria = request.POST['categoria']
        f_descripcio = request.POST['descripcio']
        f_localitat = request.POST['localitat']
        festa = Festes(nom=f_nom, data_inici=f_data_inici, data_fi=f_data_fi, categoria=f_categoria,
            descripcio=f_descripcio, localitat=f_localitat)
        festa.save()
        org.festa.add(festa)
        festa_id = 'festes/' + str(festa.id) + '.html'
        return HttpResponseRedirect(festa_id)
    elif request.method == 'GET':
        organitzadors = Organitzadors.objects.all()
        org = False
        if request.user in organitzadors:
            org = True
        festes = Festes.objects.all()
        if request.user.is_authenticated():
            username = request.user.username
            user = Usuaris.objects.get(username=username)
            assis = user.assistencia.all()
        else:
            assis = []
        if(format == 'html'):
            variables = Context({
                'festes': festes,
                'titlehead': 'Gestor de Festes',
                'pagetitle': 'Festes',
                'assis': assis,
                'org': org,
                })
            nff = NewFestaForm()
            return render_to_response('festes.html',
                dict(newfestaform=nff),
                context_instance=RequestContext(request, variables))
        else:
            return formate(format, festes)
    else:
        return Http405()


def festa(request, idFesta, format='html'):
    try:
        festa = Festes.objects.get(id=idFesta)
    except:
        festa = None
    if request.method == 'PUT':
        if festa == None:
            nff = NewFestaForm(request.PUT)
            user = request.user
            org = Organitzadors.objects.get(username=user.username)
            f_nom = request.POST['nom']
            f_data_inici = request.POST['data_inici']
            f_data_fi = request.POST['data_fi']
            f_categoria = request.POST['categoria']
            f_descripcio = request.POST['descripcio']
            f_localitat = request.POST['localitat']
            festa = Festes(nom=f_nom, data_inici=f_data_inici, data_fi=f_data_fi, categoria=f_categoria,
                descripcio=f_descripcio, localitat=f_localitat)
            festa.save()
            org.festa.add(festa)
            festa_id = 'festes/' + str(festa.id) + '.html'
            return HttpResponseRedirect(festa_id)
        else:
            nff = NewFestaForm(request.PUT, instance=festa)
            festa.save()
            events = Events.objects.filter(festa=festa)
            variables = Context({
                'festa': festa,
                'events': events,
                'titlehead': 'Detalls de la Festa',
                'pagetitle': festa.nom,
            })
            return render(request, "festa.html", variables)
    elif request.method == 'DELETE':
        festa.delete()
        festa.save()
    elif request.method == 'GET':
        if festa == None:
            organitzadors = Organitzadors.objects.all()
            org = False
            if request.user in organitzadors:
                org = True
            variables = Context({
                'titlehead': 'Gestor de Festes',
                'pagetitle': 'Festes',
                'org': org,
            })
            nff = NewFestaForm()
            return render_to_response('festa.html',
                dict(newfestaform=nff),
                context_instance=RequestContext(request, variables))
        else:
            organitzadors = Organitzadors.objects.all()
            org = False
            if request.user in organitzadors:
                org = True
            la_festa = Festes.objects.get(id=idFesta)
            if(format == 'html'):
                events = Events.objects.filter(festa=festa)
                variables = Context({
                    'festa': festa,
                    'events': events,
                    'titlehead': 'Detalls de la Festa',
                    'pagetitle': festa.nom,
                })
                nff = NewFestaForm()
                return render_to_response('festa.html',
                    dict(newfestaform=nff),
                    context_instance=RequestContext(request, variables))
            else:
                return formate(format, Festes.objects.filter(id=idFesta))
    else:
        return Http405()


def ubicacions(request, format='html'):
    if request.method == 'POST':
        nuf = NewUbiForm(request.POST)
        u_latitude = request.POST['latitude']
        u_longitude = request.POST['longitude']
        u_provincia = request.POST['provincia']
        u_comarca = request.POST['comarca']
        u_poble = request.POST['poble']
        u_adressa = request.POST['adressa']
        ubi = Ubicacions(latitude=u_latitude, longitude=u_longitude, provincia=u_provincia, comarca=u_comarca,
            poble=u_poble, adressa=u_adressa)
        ubi.save()
        ubi_id = 'ubicacions/' + str(ubi.id) + '.html'
        return HttpResponseRedirect(ubi_id)
    else:
        organitzadors = Organitzadors.objects.all()
        org = False
        if request.user in organitzadors:
            org = True
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
            nuf = NewUbiForm()
            return render_to_response('ubicacions.html',
                dict(newubiform=nuf),
                context_instance=RequestContext(request, variables))
        else:
            return formate(format, ubicacions)


def ubicacio(request, idUbi, format='html'):
    organitzadors = Organitzadors.objects.all()
    org = False
    if request.user in organitzadors:
        org = True
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


def ubi_update(request, idUbi):
    if request.method == 'POST':
        nuf = NewUbiForm(request.POST)
        u_latitude = request.POST['latitude']
        u_longitude = request.POST['longitude']
        u_provincia = request.POST['provincia']
        u_comarca = request.POST['comarca']
        u_poble = request.POST['poble']
        u_adressa = request.POST['adressa']
        ubi = Ubicacions(latitude=u_latitude, longitude=u_longitude, provincia=u_provincia, comarca=u_comarca,
            poble=u_poble, adressa=u_adressa)
        ubi.save()
        ubi_id = 'ubicacions/' + str(ubi.id) + '.html'
        return HttpResponseRedirect(ubi_id)
    elif request.method == 'GET':
        variables = Context({
            'ubicacio': ubicacio,
            'titlehead': 'Detalls de la Ubicacio',
            'pagetitle': ubicacio.adressa,
        })
        nff = NewFestaForm()
        return render_to_response('ubicacio.html',
            dict(newfestaform=nff),
            context_instance=RequestContext(request, variables))
    else:
            return Http405()


def events(request, format='html'):
    organitzadors = Organitzadors.objects.all()
    org = False
    if request.user in organitzadors:
        org = True
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
    organitzadors = Organitzadors.objects.all()
    org = False
    if request.user in organitzadors:
        org = True
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


from rest_framework import generics
from serializers import UbicacioSerializer

'''
class IsOwnerOrReadOnly(Permissions.BasePermission):
    def has_object_permission(self,request,view,obj):
        if request.method in permission.SAFE_METHODS:
            return True
        return obj.user == request.user'''

class APIUbicacioDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Ubicacions
    serializer_class = CiutatSerializer


class APIUbicacionsList(generics.ListCreateAPIView):
    model = Ubicacions
    serializer_class = CiutatSerializer