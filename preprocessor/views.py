# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from annoying.functions import get_object_or_None
from django.core import serializers
from django.http import JsonResponse

from .models import Location
from .utils import get_location_geometry


def location_list(request):
    if request.method == 'GET':
        locations_as_json = serializers.serialize('json', Location.objects.all())
        return JsonResponse({'location_list': locations_as_json})


def location_geometry(request):
    if request.method == 'GET':
        location_pk = request.GET['location_pk']
        location = get_object_or_None(Location, pk=location_pk)
        return JsonResponse({
            'location_geometry': json.dumps(get_location_geometry(location))
        })
