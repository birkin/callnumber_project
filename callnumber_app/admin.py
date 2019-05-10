# -*- coding: utf-8 -*-

from .models import Subject
from django.contrib import admin


class SubjectAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'code_range', 'note' )
    search_fields = ( 'id', 'name', 'code_range', 'note' )
    ordering = [ 'name' ]


admin.site.register(Subject, SubjectAdmin)
