# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import json, os


DOCS_URL = unicode( os.environ['CLLNMBR__DOCS_URL'] )

LEGIT_USER = unicode( os.environ['CLLNMBR__LEGIT_USER'] )
LEGIT_USER_PASSWORD = unicode( os.environ['CLLNMBR__LEGIT_USER_PASSWORD'] )

LEGIT_GROUPER_GROUPS = json.loads( os.environ['CLLNMBR__LEGIT_GROUPS_JSON'] )
LEGIT_EPPNS = json.loads( os.environ['CLLNMBR__LEGIT_EPPNS_JSON'] )
