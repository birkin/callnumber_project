# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['CLLNMBR__DOCS_URL']


# LEGIT_USER = os.environ['CLLNMBR__LEGIT_USER']
# LEGIT_USER_PASSWORD = os.environ['CLLNMBR__LEGIT_USER_PASSWORD']

# LEGIT_GROUPER_GROUPS = json.loads( os.environ['CLLNMBR__LEGIT_GROUPS_JSON'] )
# LEGIT_EPPNS = json.loads( os.environ['CLLNMBR__LEGIT_EPPNS_JSON'] )


## auth
SUPER_USERS = json.loads( os.environ['CLLNMBR__SUPER_USERS_JSON'] )
STAFF_USERS = json.loads( os.environ['CLLNMBR__STAFF_USERS_JSON'] )  # users permitted access to admin
STAFF_GROUP = os.environ['CLLNMBR__STAFF_GROUP']  # not grouper-group; rather, name of django-admin group for permissions
TEST_META_DCT = json.loads( os.environ['CLLNMBR__TEST_META_DCT_JSON'] )
POST_LOGIN_ADMIN_REVERSE_URL = os.environ['CLLNMBR__POST_LOGIN_ADMIN_REVERSE_URL']  # tricky; for a direct-view of a model, the string would be in the form of: `admin:APP-NAME_MODEL-NAME_changelist`
