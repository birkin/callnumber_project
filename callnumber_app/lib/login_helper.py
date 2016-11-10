# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import logging
from callnumber_app import settings_app
from callnumber_app.lib.shib import ShibChecker
from django.conf import settings
from django.contrib.auth import authenticate


log = logging.getLogger(__name__)
shib_checker = ShibChecker()


class UserGrabber(object):

    def get_user( self, meta_dct ):
        if shib_checker.validate_user( meta_dct ):
            log.debug( 'validated via shib' )
            user = self.grab_good_user()
        elif meta_dct['SERVER_NAME'] == '127.0.0.1' and settings.DEBUG == True:
            log.debug( 'validated via localdev' )
            user = self.grab_good_user()
        else:
            log.debug( 'not validated' )
            user = None
        return user

    def grab_good_user( self ):
        user = authenticate( username=settings_app.LEGIT_USER, password=settings_app.LEGIT_USER_PASSWORD )
        return user
