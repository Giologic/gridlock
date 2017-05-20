# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from annoying.functions import get_object_or_None
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from preprocessor.models import Location
from preprocessor.utils import get_location_geometry
from .computations import LatticeLayout, RandomLayout, NBlobLayout

# TODO: Refactor for consistency; sometimes its (lat, lng) at other times its (lng , lat)


@csrf_exempt
def generate_stop_layout(request):
    if request.method == 'POST':
        layout_type = request.POST['layout_type']
        max_num_stops = int(request.POST['max_num_stops'])
        max_walking_dist = float(request.POST['max_walking_dist'])

        if layout_type == 'LATTICE':
            stop_layout_nodes = generate_lattice(request, max_num_stops, max_walking_dist)
        elif layout_type == 'RANDOM':
            stop_layout_nodes = generate_random(request, max_num_stops, max_walking_dist)
        elif layout_type == 'N-BLOB':
            stop_layout_nodes = generate_nblob(request, max_num_stops, max_walking_dist)
        else:
            raise ValueError("Invalid stop layout type")

        return JsonResponse({'stop_layout_nodes': [n.__dict__ for n in stop_layout_nodes]})


def generate_lattice(request, max_num_stops, max_walking_dist):
    lattice_start_lat = float(request.POST['lattice_start_lat'])
    lattice_start_lng = float(request.POST['lattice_start_lng'])
    return LatticeLayout(max_num_stops, max_walking_dist, (lattice_start_lng, lattice_start_lat)).generate()


def generate_random(request, max_num_stops, max_walking_dist):
    location = get_object_or_None(Location, pk=1)
    location_geometry = get_location_geometry(location)
    return RandomLayout(max_num_stops, max_walking_dist, location_geometry).generate()


def generate_nblob(request, max_num_stops, max_walking_dist):
    return NBlobLayout(100, 350, [(120.9747, 14.6184), (121.0007, 14.5796)], 65).generate()
