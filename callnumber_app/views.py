# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint
from callnumber_app import settings_app
from callnumber_app.lib import view_info_helper
from callnumber_app.lib import views_helper
from callnumber_app.lib.login_helper import UserGrabber
from django.contrib.auth import login as django_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)
user_grabber = UserGrabber()


def info( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


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
    ( dump_param_handler, service_response ) = ( views_helper.DumpParamHandler(), {} )  # initialization
    if request.GET.get( 'data', '' ) == 'dump':
        return_values = dump_param_handler.grab_all_v1()
        service_response = {'data': 'dump'}
    elif 'callnumber' in request.GET:
        call_param_handler = views_helper.CallParamHandler( request.GET['callnumber'].split(',') )
        return_values = call_param_handler.grab_callnumbers()
        service_response['query'] = { 'request_type': 'call number', 'request_numbers': call_param_handler.callnumbers }
    service_response['result'] = { 'items': return_values, 'service_documentation': settings_app.DOCS_URL }
    output = json.dumps( service_response, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json')

