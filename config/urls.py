# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf.urls import include, url
from django.contrib import admin


admin.autodiscover()


urlpatterns = [

    url( r'^admin/', include(admin.site.urls) ),  # eg host/callnumber/admin/

    url( r'^', include('callnumber_app.urls_app', namespace='callnumber') ),  # eg host/callnumber/anything/

    ]
