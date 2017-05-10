# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.core import serializers
from django.http import JsonResponse

from annoying.functions import get_object_or_None
from pygeoj import load

from gridlock.settings import DATA_FILES_ROOT
from .models import Location


def location_list(request):
    if request.method == 'GET':
        locations_as_json = serializers.serialize('json', Location.objects.all())
        return JsonResponse({'location_list': locations_as_json})


def location_geometry(request):
    if request.method == 'GET':
        location_pk = request.GET['location_pk']
        location = get_object_or_None(Location, pk=location_pk)

        location_file = open(os.path.join(DATA_FILES_ROOT, location.path))
        location_json = json.load(location_file)
        return JsonResponse({'location_geometry': json.dumps(location_json)})
