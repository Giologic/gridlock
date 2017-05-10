# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import serializers
from django.http import JsonResponse

from .models import Location


def location_list(request):
    if request.method == 'GET':
        locations_as_json = serializers.serialize('json', Location.objects.all())
        return JsonResponse({'location_list': locations_as_json})


def location(request):
    if request.method == 'GET':
        pass
