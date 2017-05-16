# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from . import views

app_name = 'stopgenerator'
urlpatterns = [
    url(r'^generate_stop_layout', views.generate_stop_layout, name='generate_stop_layout'),
]
