from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core import urlresolvers

from webjukebox import utils
from webjukebox import models
from webjukebox import actions
from webjukebox import forms

import json
import logging


def index(request):
    context = utils.get_context(request)

    ########## Temporary code for creating a default username to test with
    # TODO: Remove later
    from django.contrib.auth import models as auth_models
    admin_user, created = auth_models.User.objects.get_or_create(username='admin')
    if created:
        admin_user.set_password('testpass')
        admin_user.save()
        ########## end temporary code

    #    if hasattr(context['user'], 'profile'):
    #        context['is_dj'] = context['user'].profile.is_dj

    return render_to_response('home.html', context)


def registration(request):
    context = utils.get_context(request)

    #TODO: REGISTRATION FORM HERE
    #Tom Moser calls dibs

    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            #NEED to create a method to create a user in actions.py
            user = actions.create_user(form.cleaned_data)
            return redirect('site-login')
    else:
        form = forms.RegistrationForm()

    context['form'] = form

    return render_to_response('registration.html', context)


def find_event(request):
    context = utils.get_context(request)
    zipcode = None
    events = None
    if request.method == "POST":
        form = forms.EventFinderForm(request.POST)
        if form.is_valid():
            zipcode = form.cleaned_data['zipcode']
            logging.warning(zipcode)
    else:
        form = forms.EventFinderForm()
    context['form'] = form

    if zipcode:
        events = actions.get_nearby_events(zipcode)
    context['nearby_events'] = events or None
    return render_to_response('patron/find_event.html', context)


def event_requests(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    context['libraries'] = actions.get_libraries_by_event(context['event'])
    context['session_requests'] = request.session['song-requests']
    return render_to_response('patron/event_requests.html', context)


def request_song(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    song_id = request.GET.get('song_id')
    action = request.GET.get('action')
    result = actions.request_song(context['event'], song_id, action)
    if result == 'added':
        request.session['song-requests'] = request.session['song-requests'] + [str(song_id)]
    elif result == 'removed':
        if song_id in request.session['song-requests']:
            request.session['song-requests'].remove(str(song_id))
    return HttpResponse(
        json.dumps({'song_id':song_id, 'result':result}), mimetype="application/json")
