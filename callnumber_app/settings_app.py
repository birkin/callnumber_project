# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, os


LEGIT_USER = os.environ['CLLNMBR__LEGIT_USER']
LEGIT_USER_PASSWORD = os.environ['CLLNMBR__LEGIT_USER_PASSWORD']

LEGIT_GROUPER_GROUPS = json.loads( os.environ['CLLNMBR__LEGIT_GROUPS_JSON'] )
LEGIT_EPPNS = json.loads( os.environ['CLLNMBR__LEGIT_EPPNS_JSON'] )
