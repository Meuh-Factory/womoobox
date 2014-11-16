from django.shortcuts import render
from womoobox.models import *
from womoobox.settings import *
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.db import models
from django import forms
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from django.core import serializers
from womoobox.forms import *
from datetime import timedelta, datetime
from django.utils.timezone import now, make_aware, get_current_timezone
from womoobox.errors import *
from django.conf import settings


# Api documentation
def api_index(request):
    if request.user.is_staff:
        return render(request, 'api.html', {})
    else: # only allow authenticated users with staff membership
        return HttpResponseForbidden("Erreur HTTP 403 Forbidden")


# Create a new Moo
@csrf_exempt # no csrf check in forms
@xframe_options_exempt # no x-frame-options header (api available from other domains)
def moo_add(request):
    if request.method == 'POST':
        form_moo = MooForm(request.POST)
        if not form_moo.is_valid():
            # invalid inputs
            return format_error(INVALID_INPUT_VALUE)
        form_key = form_moo.cleaned_data['key']
        # test API Key
        try:
            key = ApiKey.objects.get(key=form_key) # search in backend
        except ApiKey.DoesNotExist:
            # unknown API key
            return format_error(INVALID_KEY)
        if key.blacklisted: # is the key blacklisted
            return format_error(BLACKLISTED_KEY)
        # form inputs to variables
        form_lat = form_moo.cleaned_data['latitude']
        form_lon = form_moo.cleaned_data['longitude']
        form_ani = form_moo.cleaned_data['animal']
        # limit set of lat/lon inputs
        if (form_lat < -90) or (form_lat > 90) or (form_lon < -180) or (form_lon > 180):
            return format_error(INVALID_COORDS_VALUE)
        # check if no too recent Moo of same user/animal
        limit = now() - timedelta(minutes=MIN_DURATION_BETWEEN_MOO)
        if Moo.objects.filter(key=key,
                              animal_type=form_ani,
                              creation_date__gt=limit):
            return format_error(TOO_MOO_SHORT_TIME)
        # new Moo object from information in form
        moo = Moo(key = key,
                  latitude = form_lat,
                  longitude = form_lon,
                  animal_type = form_ani)
        moo.save()
        return format_success( {'id': moo.id })
    else: # GET
        if settings.DEBUG:
            f = MooForm()
            return render(request, 'moo_form.html', {'form': f.as_table()})
        else:
            return HttpResponseNotAllowed(['POST'])


# Get count of Moos in the world
@csrf_exempt
def moo_get_count(request):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    nb_moos = Moo.objects.count()
    response = { 'nb_moos' : nb_moos }
    return JsonResponse(response)


# Get last Moo (+from a reference ID)
@csrf_exempt
def moo_get_lasts(request, *args, **kwargs):
    if request.method != 'GET':
        return HttpResponseNotAllowed(['GET'])
    form_get_moo = GetMooForm(request.GET)
    form_get_moo.is_valid()
    if not form_get_moo.is_valid():
        return format_error(INVALID_INPUT_VALUE)
    # id checking
    limit = form_get_moo.cleaned_data['id']
    if limit:
        if limit <= Moo.objects.all().count():
            # select Moos based on this id filter
            moos = Moo.objects.filter(id__gt=limit)[:MAX_NUMBER_OF_MOO]
        else:
           return format_error(INVALID_ID)
    else:
        # if no ID filter, return last Moos
        moos = Moo.objects.all()[:MAX_NUMBER_OF_INITIAL_MOO]
    # create response object
    json_moos = []
    for moo in moos:
        j_moo = {
            'id'            : moo.id,
            'latitude'      : str(moo.latitude),
            'longitude'     : str(moo.longitude),
            'animal'        : moo.animal_type,
            'username'      : moo.key.user_name
        }
        json_moos.append(j_moo)
    response = { 'moos' : json_moos }
    return JsonResponse(response)


@csrf_exempt # no csrf check in forms
@xframe_options_exempt # no x-frame-options header (api available from other domains)
def key_add(request):
    # create an API key
    key = ApiKey(user_agent=request.META['HTTP_USER_AGENT'])
    key.save()
    return format_success({ 'key': key.key,
                            'user_name': key.user_name })


# Rename ApiKey
@csrf_exempt # no csrf check in forms
@xframe_options_exempt # no x-frame-options header (api available from other domains)
def key_rename(request):
    if request.method == 'POST':
        form_key = KeyRename(request.POST)
        if not form_key.is_valid():
            # invalid inputs
            return format_error(INVALID_INPUT_VALUE)
        key_form_form = form_key.cleaned_data['key']
        old_username = form_key.cleaned_data['old_username']
        new_username = form_key.cleaned_data['new_username']
        # test API Key
        try:
            key = ApiKey.objects.get(key=key_form_form) # search in backend
        except ApiKey.DoesNotExist:
            # unknown API key
            return format_error(INVALID_KEY)
        # test username
        if key.user_name != old_username:
            return format_error(INVALID_USERNAME)
        try:
            ApiKey.objects.get(user_name=new_username)
            return format_error(ALREADY_EXISTING_USERNAME)
        except ApiKey.DoesNotExist:
            pass
        # rename and save
        key.user_name = new_username
        key.save()
        return format_success({ 'key': key.key,
                                'user_name': key.user_name })
    else: # GET
        if settings.DEBUG:
            f = KeyRename()
            return render(request, 'rename_form.html', {'form': f.as_table()})
        else:
            return HttpResponseNotAllowed(['POST'])