# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime, json, logging, os, pprint
from callnumber_app.lib.login_helper import UserGrabber
from django.contrib.auth import login as django_login
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)
user_grabber = UserGrabber()


def hi( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )


def assign_subject( request ):
    url = reverse('admin:callnumber_app_subject_changelist' )
    return HttpResponseRedirect( url )


def login( request ):
    log.debug( 'starting login()' )
    user = user_grabber.get_user( request.META )
    if user:
        log.debug( 'logging in user' )
        django_login(request, user )
    url = reverse('admin:callnumber_app_subject_changelist' )
    return HttpResponseRedirect( url )
