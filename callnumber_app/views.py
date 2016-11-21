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
        # resp = dump_param_handler.resp_template
        resp = {
            'query': {
                'timestamp': unicode(datetime.datetime.now()),
                'params': 'data=dump' },
            'response': {
                'documentation': 'coming',
                'items': [],
                'timestamp': None }
            }
        return_values = dump_param_handler.grab_all_v2()
    elif 'callnumber' in request.GET:
        resp = {
            'query': {
                'timestamp': unicode(datetime.datetime.now()),
                'params': 'callnumber={}'.format(pprint.pformat(request.GET['callnumber'])) },
            'response': {
                'documentation': 'coming',
                'items': [],
                'perceived_callnumbers': [],
                'timestamp': None
                }
            }
        call_param_handler = views_helper.CallParamHandler()
        callnumbers = request.GET['callnumber'].split(',')
        callnumbers.sort()
        resp['response']['perceived_callnumbers'] = callnumbers
        return_values = call_param_handler.grab_callnumbers( callnumbers )
    resp['response']['items'] = return_values
    resp['response']['timestamp'] = unicode( datetime.datetime.now() )
    output = json.dumps( resp, sort_keys=True, indent=2 )
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



# def data( request ):
#     params = request.GET
#     service_request = params['data']
#     return_values = []
#     if service_request == 'dump':
#         service_response = {'data': 'dump'}
#         all = Subject.objects.all()
#         return_dict = {}
#         for sub in all:
#             return_dict[sub.id] = {}
#             return_dict[sub.id]['name'] = sub.name
#             return_dict[sub.id]['code_range'] = sub.code_range
#             return_dict[sub.id]['slug'] = sub.slug
#             return_dict[sub.id]['points'] = []
#             for crange in sub.code_range.split(','):
#                 points = crange.strip().split('-')
#                 # start = normalize_call_number(points[0])
#                 start = callnumber_normalizer.normalize( points[0] )
#                 if len(points) == 2:
#                     # stop = normalize_call_number(points[1].replace('.999', '.99'))
#                     stop = callnumber_normalizer.normalize( points[1].replace('.999', '.99') )
#                 else:
#                     stop = None
#                 return_dict[sub.id]['points'].append({
#                                                       'start': start,
#                                                       'stop': stop})
#         return_values = return_dict
#     else:
#         return HttpResponse('error')

#     service_response['result'] = {}
#     service_response['result']['items'] = return_values
#     service_response['result']['service_documentation'] = 'coming soon'
#     service_response['result']['service_contact'] = 'coming soon'
#     output = json.dumps( service_response, sort_keys=True, indent=2 )
#     return HttpResponse( output, content_type='application/json')
