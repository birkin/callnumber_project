# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint
from callnumber_app.lib.login_helper import UserGrabber
from django.contrib.auth import login as django_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
# from callnumber_app.models import Subject
# from callnumber_app.lib import callnumber_normalizer, views_helper
from callnumber_app.lib import views_helper


log = logging.getLogger(__name__)
user_grabber = UserGrabber()


def hi( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )


def login( request ):
    log.debug( 'starting login()' )
    user = user_grabber.get_user( request.META )
    if user:
        log.debug( 'logging in user' )
        django_login(request, user )
    url = reverse('admin:callnumber_app_subject_changelist' )
    log.debug( 'redirect url to admin, ```{}```'.format(url) )
    return HttpResponseRedirect( url )  ## TODO: add shib logout (via redirecting to shib-logout url, then redirecting to the above admin url)


def data_v2( request ):
    """ Handles all /v2/ urls. """
    if request.GET.get( 'data', '' ) == 'dump':
        dump_param_handler = views_helper.DumpParamHandler()
        resp = dump_param_handler.resp_template
        return_values = dump_param_handler.grab_all_v2()
    elif 'callnumber' in request.GET:
        call_param_handler = views_helper.CallParamHandler( request.GET['callnumber'].split(',') )
        resp = call_param_handler.resp_template
        return_values = call_param_handler.grab_callnumbers()
    output = views_helper.prep_jsn( resp, return_values )
    return HttpResponse( output, content_type='application/json')


def data_v1( request ):
    """ Handles all /v1/ urls. """
    dump_param_handler = views_helper.DumpParamHandler()
    service_response = {}
    if request.GET.get( 'data', '' ) == 'dump':
        return_values = dump_param_handler.grab_all_v1()
        service_response = {'data': 'dump'}

    elif 'callnumber' in request.GET:
        call_param_handler = views_helper.CallParamHandler()
        return_values = call_param_handler.grab_callnumbers( request.GET['callnumber'].split() )
    service_response['result'] = {}
    service_response['result']['items'] = return_values
    service_response['result']['service_documentation'] = 'coming soon'
    service_response['result']['service_contact'] = 'coming soon'
    output = json.dumps( service_response, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json')
