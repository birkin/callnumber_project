# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint
from django.conf import settings as project_settings
from django.core.urlresolvers import reverse
from django.db import models
from django.http import HttpResponseRedirect

log = logging.getLogger(__name__)


class Subject(models.Model):

    name = models.CharField( max_length=100 )
    slug = models.SlugField()
    code_range = models.TextField()
    note = models.TextField( blank=True )

    def __unicode__(self):
        return '%s' % self.name
