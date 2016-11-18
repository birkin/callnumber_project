# -*- coding: utf-8 -*-

from __future__ import unicode_literals
""" Holds code supporting views.py """

from callnumber_app.models import Subject
from callnumber_app.lib import callnumber_normalizer


class DumpParamHandler(object):
    """ Handles request.GET['data'] = 'dump'
        Called by views.data() """

    def __init__( self ):
        pass

    def grab_all( self ):
        """ Prepares all callnumber info from db.
            Called by views.data() """
        subjects = Subject.objects.all()
        return_dict = {}
        for sub in subjects:
            return_dict[sub.id] = {}
            return_dict[sub.id]['name'] = sub.name
            return_dict[sub.id]['code_range'] = sub.code_range
            return_dict[sub.id]['slug'] = sub.slug
            return_dict[sub.id]['points'] = []
            for crange in sub.code_range.split(','):
                points = crange.strip().split('-')
                start = callnumber_normalizer.normalize( points[0] )
                if len(points) == 2:
                    stop = callnumber_normalizer.normalize( points[1].replace('.999', '.99') )
                else:
                    stop = None
                return_dict[sub.id]['points'].append( {'start': start, 'stop': stop} )
        return return_dict
