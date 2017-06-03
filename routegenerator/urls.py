# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

app_name = 'routegenerator'
urlpatterns = [
    url(r'^generate_route_network', views.generate_route_network, name='generate_route_network'),
    url(r'^generate_route', views.generate_route, name='generate_route')
]
