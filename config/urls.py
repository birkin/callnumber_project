# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',

    url( r'^admin/', include(admin.site.urls) ),  # eg host/callnumber/admin/

    url( r'^', include('callnumber_app.urls_app') ),  # eg host/callnumber/anything/

)
