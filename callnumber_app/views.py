# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from callnumber_app import settings_app
from callnumber_app.lib.shib import ShibChecker
from callnumber_app.lib import login
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render


log = logging.getLogger(__name__)
shib_checker = ShibChecker()


def hi( request ):
    """ Returns simplest response. """
    now = datetime.datetime.now()
    return HttpResponse( '<p>hi</p> <p>( %s )</p>' % now )


def assign_subject( request ):
    url = reverse('admin:callnumber_app_subject_changelist' )
    return HttpResponseRedirect( url )


def login( request ):
    log.debug( 'starting login()' )
    # user = lib.get_user( request.META )
    if shib_checker.validate_user( request.META ):
        log.debug( 'validated via shib' )
        user = authenticate(username=settings_app.LEGIT_USER, password=settings_app.LEGIT_USER_PASSWORD)
    elif request.META['SERVER_NAME'] == '127.0.0.1' and settings.DEBUG == True:
        log.debug( 'validated via localdev' )
        user = authenticate(username=settings_app.LEGIT_USER, password=settings_app.LEGIT_USER_PASSWORD)
    else:
        user = None
    if user:
        django_login(request, user )
    url = reverse('admin:callnumber_app_subject_changelist' )
    return HttpResponseRedirect( url )
