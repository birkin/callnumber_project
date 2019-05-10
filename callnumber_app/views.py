# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from callnumber_app import settings_app
from callnumber_app.lib import common
from callnumber_app.lib import view_info_helper
from callnumber_app.lib import views_helper
from callnumber_app.lib.login_helper import UserGrabber
from callnumber_app.lib.shib_auth import shib_login  # decorator
from django.conf import settings as project_settings
from django.contrib.auth import login as django_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)
user_grabber = UserGrabber()


@shib_login
def login( request ):
    """ Handles authNZ, & redirects to admin.
        Called by click on login or admin link. """
    next_url = request.GET.get( 'next', None )
    if not next_url:
        redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
    else:
        redirect_url = request.GET['next']  # will often be same page
    log.debug( 'login redirect url, ```%s```' % redirect_url )
    return HttpResponseRedirect( redirect_url )


# def data_v2( request ):
#     """ Handles all /v2/ urls. """
#     if request.GET.get( 'data', '' ) == 'dump':
#         dump_param_handler = views_helper.DumpParamHandler()
#         resp = dump_param_handler.resp_template
#         return_values = dump_param_handler.grab_all_v2()
#     elif 'callnumber' in request.GET:
#         call_param_handler = views_helper.CallParamHandler( request.GET['callnumber'].split(',') )
#         resp = call_param_handler.resp_template
#         return_values = call_param_handler.grab_callnumbers()
#     output = views_helper.prep_jsn( resp, return_values )
#     return HttpResponse( output, content_type='application/json')


def data_v2( request ):
    """ Handles all /v2/ urls. """
    ( rq_now, rq_url ) = ( datetime.datetime.now(), common.make_request_url(request) )  # initializer
    if request.GET.get( 'data', '' ) == 'dump':
        dump_param_handler = views_helper.DumpParamHandler( rq_now, rq_url )
        resp = dump_param_handler.resp_template
        return_values = dump_param_handler.grab_all_v2()
    elif 'callnumber' in request.GET:
        call_param_handler = views_helper.CallParamHandler( request.GET['callnumber'].split(','), rq_now, rq_url )
        resp = call_param_handler.resp_template
        return_values = call_param_handler.grab_callnumbers()
    output = views_helper.prep_jsn( resp, return_values, rq_now )
    return HttpResponse( output, content_type='application/json')


def data_v1( request ):
    """ Handles all /v1/ urls. """
    ( service_response, rq_now, rq_url ) = ( {}, datetime.datetime.now(), common.make_request_url(request) )  # initialization
    dump_param_handler = views_helper.DumpParamHandler( rq_now, rq_url )
    if request.GET.get( 'data', '' ) == 'dump':
        return_values = dump_param_handler.grab_all_v1()
        service_response = {'data': 'dump'}
    elif 'callnumber' in request.GET:
        call_param_handler = views_helper.CallParamHandler( request.GET['callnumber'].split(','), rq_now, rq_url )
        return_values = call_param_handler.grab_callnumbers()
        service_response['query'] = { 'request_type': 'call number', 'request_numbers': call_param_handler.callnumbers }
    service_response['result'] = { 'items': return_values, 'service_documentation': settings_app.README_URL }
    output = json.dumps( service_response, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json')


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


def error_check( request ):
    """ For checking that admins receive error-emails. """
    if project_settings.DEBUG == True:
        1/0
    else:
        return HttpResponseNotFound( '<div>404 / Not Found</div>' )
