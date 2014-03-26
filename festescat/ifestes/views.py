# Create your views here.

from django.http import HttpResponse, Http404
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from django.shortcuts import render_to_response

def mainpage(request):
    template = get_template('mainpage.html')
    variables = Context({
        'titlehead': 'Festes.cat',
        'pagetitle': 'Welcome to the Festes.cat aPPlication',
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

def list_festes(request):
    return render_to_response('festes.html')