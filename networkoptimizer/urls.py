# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

app_name = 'networkoptimizer'
urlpatterns = [
    url(r'^check_fitness_score', views.check_fitness_score, name='check_fitness_score'),
    url(r'^optimize_route_network', views.optimize_route_network, name='optimize_route_network'),
]
