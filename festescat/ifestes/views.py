# Create your views here.

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import Context, RequestContext
from django.template.loader import get_template
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.utils.decorators import method_decorator
from django.shortcuts import render, render_to_response, get_object_or_404
from django.core import serializers
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from ifestes.models import *
from ifestes.forms import *


class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class CheckIsOrganitzador(object):
    def get_object(self, *args, **kwargs):
        obj = super(CheckIsOrganitzador, self).get_object(*args, **kwargs)
        #if not isinstance(obj, Organitzadors):
        #    raise PermissionDenied
        return obj


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
        festes = user.assistencia.all()
        variables = Context({
            'user': request.user,
            'username': username,
            'festes': festes
            })
        return render_to_response('userpage.html',
            dict(userform=uf),
            context_instance=RequestContext(request, variables))


def org(request, username):
    if request.method == 'POST':
        of = OrgForm(request.POST, prefix='org')
        user = Usuaris.objects.get(username=username)
        empresa = request.POST['org-empresa']
        org = Organitzadors(usuaris_ptr=user, username=user.username,
            email=user.email, password=user.password, empresa=empresa)
        org.empresa = empresa
        org.save()
        g = Group.objects.get(name='Organitzadors')
        g.user_set.add(org)
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
            user.set_password(user_password)
            user.save()
            g = Group.objects.get(name='Usuaris')
            g.user_set.add(user)
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
        nff = FestaForm(request.POST)
        user = request.user
        org = Organitzadors.objects.get(username=user.username)
        f_nom = request.POST['nom']
        f_data_inici = request.POST['data_inici']
        f_data_fi = request.POST['data_fi']
        f_categoria = request.POST['categoria']
        f_descripcio = request.POST['descripcio']
        f_localitat = request.POST['localitat']
        festa = Festes(nom=f_nom, data_inici=f_data_inici,
            data_fi=f_data_fi, categoria=f_categoria,
            descripcio=f_descripcio, localitat=f_localitat)
        festa.save()
        org.festa.add(festa)
        festa_id = '/festes/' + str(festa.id) + '/'
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
            nff = FestaForm()
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
        if festa is None:
            nff = FestaForm(request.PUT)
            user = request.user
            org = Organitzadors.objects.get(username=user.username)
            f_nom = request.POST['nom']
            f_data_inici = request.POST['data_inici']
            f_data_fi = request.POST['data_fi']
            f_categoria = request.POST['categoria']
            f_descripcio = request.POST['descripcio']
            f_localitat = request.POST['localitat']
            festa = Festes(nom=f_nom, data_inici=f_data_inici,
                data_fi=f_data_fi, categoria=f_categoria,
                descripcio=f_descripcio, localitat=f_localitat)
            festa.save()
            org.festa.add(festa)
            festa_id = '/festes/' + str(festa.id) + '/'
            return HttpResponseRedirect(festa_id)
        else:
            nff = FestaForm(request.PUT, instance=festa)
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
        if festa is None:
            organitzadors = Organitzadors.objects.all()
            org = False
            if request.user in organitzadors:
                org = True
            variables = Context({
                'titlehead': 'Gestor de Festes',
                'pagetitle': 'Festes',
                'org': org,
            })
            nff = FestaForm()
            return render_to_response('festa.html',
                dict(newfestaform=nff),
                context_instance=RequestContext(request, variables))
        else:
            organitzadors = Organitzadors.objects.all()
            org = False
            if request.user in organitzadors:
                org = True
            festa = Festes.objects.get(id=idFesta)
            if(format == 'html'):
                return HttpResponseRedirect('/festes/' + str(idFesta) + '/')
            else:
                return formate(format, Festes.objects.filter(id=idFesta))
    else:
        return HttpResponseNotAllowed()


def assist(request, idFesta):
    if request.method == 'POST':
        user = Usuaris.objects.get(username=request.user.username)
        festa = Festes.objects.get(id=idFesta)
        user.assistencia.add(festa)
        user.save()
        return HttpResponseRedirect('/festes/')
    else:
        return HttpResponseNotAllowed()


def no_assist(request, idFesta):
    if request.method == 'POST':
        user = Usuaris.objects.get(username=request.user.username)
        festa = Festes.objects.get(id=idFesta)
        user.assistencia.remove(festa)
        return HttpResponseRedirect('/festes/')
    else:
        return HttpResponseNotAllowed()


class UserUpdateView(UpdateView):
    model = Usuaris
    template_name = 'form.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class OrganitzadorUpdateView(LoginRequiredMixin, UpdateView):
    model = Organitzadors
    template_name = 'form.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


class FestaDetail(DetailView):
    model = Festes
    template_name = 'festa.html'


class FestaDelete(LoginRequiredMixin, CheckIsOrganitzador, DeleteView):
    model = Festes
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('festes')


class UbicacioDetail(DetailView):
    model = Ubicacions
    template_name = 'ubicacio.html'


class UbicacioDelete(LoginRequiredMixin, CheckIsOrganitzador, DeleteView):
    model = Ubicacions
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('ubicacions')


class LoginRequiredCheckIsOrganitzadorCreateView(LoginRequiredMixin,
    CheckIsOrganitzador, CreateView):
        template_name = 'form.html'


class LoginRequiredCheckIsOrganitzadorUpdateView(LoginRequiredMixin,
    CheckIsOrganitzador, UpdateView):
        template_name = 'form.html'


class EventDetail(DetailView):
    model = Events
    template_name = 'event.html'


class EventDelete(LoginRequiredMixin, CheckIsOrganitzador, DeleteView):
    model = Events
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('events')


def ubicacions(request, format='html'):
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
            'org': org,
            })
        nuf = UbiForm()
        return render_to_response('ubicacions.html',
            dict(ubiform=nuf),
            context_instance=RequestContext(request, variables))
    else:
        return formate(format, ubicacions)


def ubicacio(request, idUbi, format='html'):
    if(format == 'html'):
        return HttpResponseRedirect('/ubicacions/' + str(idUbi) + '/')
    else:
        return formate(format, Ubicacions.objects.filter(id=idUbi))


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
            'org': org,
            })
        nef = EventForm()
        return render_to_response('events.html',
            dict(eventform=nef),
            context_instance=RequestContext(request, variables))
    else:
        return formate(format, events)


def event(request, idEvent, format='html'):
    if(format == 'html'):
        return HttpResponseRedirect('/events/' + str(idEvent) + '/')
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
from .serializers import *


#class IsOwnerOrReadOnly(Permissions.BasePermission):
    #def has_object_permission(self,request,view,obj):
        #if request.method in permission.SAFE_METHODS:
            #return True
        #return obj.user == request.user

class APIUbicacioDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Ubicacions
    serializer_class = UbicacioSerializer


class APIUbicacionsList(generics.ListCreateAPIView):
    model = Ubicacions
    serializer_class = UbicacioSerializer


class APIEventDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Events
    serializer_class = EventSerializer


class APIEventsList(generics.ListCreateAPIView):
    model = Events
    serializer_class = EventSerializer


class APIFestaDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Festes
    serializer_class = FestaSerializer


class APIFestesList(generics.ListCreateAPIView):
    model = Festes
    serializer_class = FestaSerializer