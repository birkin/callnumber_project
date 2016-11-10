# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import datetime, json, logging, os, pprint
from callnumber_app import settings_app
from callnumber_app.lib.shib import ShibChecker
from django.contrib.auth import authenticate, login
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
    if shib_checker.validate_user( request.META ):
        user = authenticate(username=settings_app.LEGIT_USER, password=settings_app.LEGIT_USER_PASSWORD)
    elif request.META['SERVER_NAME'] == '127.0.0.1' and settings.DEBUG == True:
        user = authenticate(username=settings_app.LEGIT_USER, password=settings_app.LEGIT_USER_PASSWORD)
    else:
        user = None
    if user:
        login(request, user )
    url = reverse('admin:callnumber_app_subject_changelist' )
    return HttpResponseRedirect( url )
