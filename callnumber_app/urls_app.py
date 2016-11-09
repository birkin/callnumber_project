# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from callnumber_app import views
from django.conf.urls import include, url
from django.views.generic import RedirectView


urlpatterns = [

    url( r'^info/$', views.hi, name='info_url' ),

    url( r'^v1/', views.assign_subject, name='assign_url' ),

    url( r'^$',  RedirectView.as_view(pattern_name='callnumber:info_url') ),

    ]
