# -*- coding: utf-8 -*-

from __future__ import unicode_literals
""" Holds code supporting views.py """

import logging
from callnumber_app.models import Subject
from callnumber_app.lib import callnumber_normalizer


log = logging.getLogger(__name__)


class CallParamHandler(object):
    """ Handles request.GET['data'] = 'callnumber'
        Called by views.data() """

    def __init__( self ):
        self.service_response = None

    def grab_callnumbers( self, callnumbers ):
        self.service_response = {
            'request_type': 'call number', 'request_numbers': callnumbers}
        return_values = []
        for call_number in callnumbers:
            # normalized_call_number = normalize_call_number(call_number)
            normalized_call_number = callnumber_normalizer.normalize( call_number )
            subjects = self.assign_subjects( normalized_call_number, self.load_subjects() )
            return_dict = {}
            return_dict['call_number'] = call_number
            return_dict['normalized_call_number'] = normalized_call_number
            assigned_subjects = []
            for sub in subjects:
                assigned_subjects.append(Subject.objects.get(slug=sub).name)
            return_dict['brown_disciplines'] = assigned_subjects
            return_values.append(return_dict)
        # if params.has_key('sort'):
        #     if params['sort'] == 'true':
        #         return_values = sorted(return_values, key=lambda k: k['call_number'])
        return return_values

    def assign_subjects(self, callnumber, subject_groupings):
        try:
            normalized_call_number = callnumber_normalizer.normalize(callnumber)
        except Exception as e:
            log.debug( 'could not normalize callnumber, `{}`'.format(callnumber) )
            normalized_call_number = None
        #Return empty subject list if call number normalization fails
        if not normalized_call_number:
            return []
        subject_list = []
        #print subject_groupings
        for subject, start, end in subject_groupings:
          end = end.replace('.999', '.99')
          normalized_start = callnumber.normalize(start)
          normalized_end = callnumber.normalize(end)
          #Check to to see if the normalized call number is between start and end range
          this_group = normalized_start <= normalized_call_number <= normalized_end
          if this_group:
            subject_list.append(subject)
        return subject_list

    def load_subjects( self ):
        """Calls local database containing subject/discipline breakdowns.
        Returns a tuple with three elements:
        subject, start range, end range."""
        subject_groupings = []

        for group in Subject.objects.all():
            crange = group.code_range
            #Make the name the PK for later inserting.
            name = group.slug
            for range_break in crange.split(','):
                ranges = range_break.split('-')
                range_length = len(ranges)
                if range_length == 1:
                    start = ranges[0].strip()
                    end = ranges[0].strip()
                else:
                    start = ranges[0].strip()
                    end = ranges[1].strip()
                subject_groupings.append((name, start, end))
        return subject_groupings

    ## end class CallParamHandler()


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