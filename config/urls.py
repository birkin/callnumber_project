# -*- coding: utf-8 -*-

from callnumber_app import views
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView



admin.autodiscover()


urlpatterns = [

    url( r'^info/$', views.info, name='info_url' ),

    url( r'^v1/', views.data_v1, name='data_v1_url' ),

    url( r'^v2/', views.data_v2, name='data_v2_url' ),

   url( r'^admin/login/', RedirectView.as_view(pattern_name='login_url') ),

    url( r'^admin/', admin.site.urls ),

    url( r'^login/$', views.login, name='login_url' ),

    url( r'^$', RedirectView.as_view(pattern_name='info_url') ),

    ]
