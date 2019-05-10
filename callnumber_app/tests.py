# -*- coding: utf-8 -*-

import logging, pprint
from django.test import TestCase


log = logging.getLogger(__name__)
TestCase.maxDiff = None


class ClientTest( TestCase ):
    """ Tests views via Client. """

    def test_callnumber_response(self):
        """ Checks two submitted callnumbers. """
        response = self.client.get( '/v2/', { 'callnumber': 'TP1085,PJ 1001'} )
        log.debug( 'response.__dict__, ```%s```' % pprint.pformat(response.__dict__) )
        self.assertEqual( 200, response.status_code )
        content = response.content.decode('utf-8')
        self.assertTrue( '"normalized_call_number": "TP 1085"' in content )
        self.assertTrue( '"normalized_call_number": "PJ 1001"' in content )

    def test_callnumber_response(self):
        """ Checks two submitted callnumbers. """
        response = self.client.get( '/v2/', { 'callnumber': 'TP1085,PJ 1001'} )
        log.debug( 'response.__dict__, ```%s```' % pprint.pformat(response.__dict__) )
        self.assertEqual( 200, response.status_code )
        content = response.content.decode('utf-8')
        self.assertTrue( '"normalized_call_number": "TP 1085"' in content )
        self.assertTrue( '"normalized_call_number": "PJ 1001"' in content )

    ## end class ClientTest()


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    # end class RootUrlTest()


## TODO:
## - test views_helper.DumpParamHandler.prep_points()
