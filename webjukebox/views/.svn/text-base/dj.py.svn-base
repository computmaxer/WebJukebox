from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core import urlresolvers

from webjukebox import utils
from webjukebox import models
from webjukebox import actions
from webjukebox import forms

import json
import logging


def account_settings(request):
    context = utils.get_context(request)
    if not context['user'].is_authenticated():
        return redirect('account-registration')
    
    if request.method =="POST":
        form = forms.EditAccountForm(context['user'],request.POST)
        if form.is_valid():
            actions.update_user(form.cleaned_data,context['user'])
        else:
            context['dialog_open']=True
    else:
        form = forms.EditAccountForm(context['user'],initial={
            'username': request.user.username,
            'email': request.user.email,
            'firstname': request.user.first_name,
            'lastname': request.user.last_name,
            'streetaddress': request.user.profile.streetaddress,
            'city': request.user.profile.city,
            'zipcode': request.user.profile.zipcode,
            'is_dj': request.user.profile.is_dj,
        })
    context['form'] = form
    
    return render_to_response('account_settings.html', context)

def view_songs_in_library(request, library_id):
    context = utils.get_context(request)
    context['library'] = actions.get_library_by_id(library_id)
    return render_to_response('dj/library/songs.html', context)

def view_libraries(request):
    context = utils.get_context(request)
    if not context['user'].is_authenticated():
        return redirect('account-registration')
    context['user_libraries'] = actions.get_libraries_for_user(context['user'])
    
    if request.method == "POST":
        if request.POST['action'] == "create":
            add_form = forms.AddLibraryForm(request.POST, request.FILES)
            edit_form = forms.EditLibraryForm() 
            if add_form.is_valid():
                actions.read_library_file_upload(add_form.cleaned_data, context['user'])
                return redirect('view-libraries')
        elif request.POST['action'] == "edit":
            edit_form = forms.EditLibraryForm(request.POST)
            add_form = forms.AddLibraryForm()
            if edit_form.is_valid():
                actions.edit_library(edit_form.cleaned_data)
                return redirect('view-libraries')
    else:
        add_form = forms.AddLibraryForm()
        edit_form = forms.EditLibraryForm()    
    
    context['add_form'] = add_form
    context['edit_form'] = edit_form
    
    return render_to_response('dj/libraries.html', context)

def delete_library(request):
    if request.method == "POST":
        library = request.POST['library_id']
        actions.delete_library(library)
    return redirect('view-libraries')

def select_event(request):
    context = utils.get_context(request)
    if not context['user'].is_authenticated():
        return redirect('account-registration')
    context['create_open'] = request.GET.get('create', None)

    if request.method == "POST":
    #this is where we handle the form being submitted
        form = forms.CreateEventForm(context['user'], request.POST)
        if form.is_valid():
            #save the stuff in the form
            event = actions.create_event(form.cleaned_data, context['user'])
            form = forms.CreateEventForm(context['user']) #reset form
            return redirect('select-event')
    else:
        form = forms.CreateEventForm(context['user'])

    context['form'] = form

    context['user_events'] = actions.get_events_for_user(context['user'])
    return render_to_response('dj/events.html', context)


def event_requests(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    context['requested_songs'] = actions.get_song_requests_for_event(context['event'])
    context['active_pill'] = 'requests'
    return render_to_response('dj/event/requests.html', context)

def update_event_request_status(request, *args, **kwargs):
    request_id = request.GET.get('request_id')
    action = request.GET.get('action')
    result = actions.update_request_status(request_id, action)
    return HttpResponse(json.dumps({'result': result, 'request_id':request_id}), mimetype="application/json")

def event_displays(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    event = context['event']
    context['active_pill'] = 'displays'
    return render_to_response('dj/event/displays.html', context)

def display_qrcode(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    event = context['event']
    context['full_url'] = request.build_absolute_uri(urlresolvers.reverse('patron-event-requests', kwargs={'event_id':event.id}))
    return render_to_response('dj/event/qrcode.html', context)

def event_statistics(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    context['all_requests'] = actions.get_all_event_requests(context['event'])
    context['artist_stats'] = actions.get_artist_stats(context['event'])
    context['active_pill'] = 'statistics'
    return render_to_response('dj/event/statistics.html', context)


def event_setup(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    event = context['event']
    context['event-setup-form'] = forms.BaseEventForm(initial=event.__dict__)
    context['user_libraries'] = actions.get_libraries_for_user(context['user'])
    context['event_libraries'] = list(event.library_keys)
    context['active_pill'] = 'setup'
    return render_to_response('dj/event/setup.html', context)


def event_libraries_setup(request, *args, **kwargs):
    context = utils.get_event_context(request, **kwargs)
    library_id = kwargs.get('library_id')
    event = context['event']
    result = 'none'
    if request.GET.get('action') == 'add':
        if library_id not in event.library_keys:
            event.library_keys.append(library_id)
            event.save()
            result = 'added'
    elif request.GET.get('action') == 'remove':
        if library_id in event.library_keys:
            event.library_keys.remove(library_id)
            event.save()
            result = 'removed'
    return HttpResponse(json.dumps({'result': result}), mimetype="application/json")