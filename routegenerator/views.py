# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import computations
import json

from json_tricks import dumps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from stopgenerator.utils import convert_latlng_to_stop_nodes
from .utils import snap_route_network_to_road


@csrf_exempt
def generate_route_network(request):
    stop_node_coordinates = json.loads(request.POST['stop_node_coordinates'])
    stop_nodes = convert_latlng_to_stop_nodes(stop_node_coordinates)
    maximum_walking_distance = float(request.POST['maximum_walking_distance'])
    number_of_generations = int(request.POST['number_of_generations'])

    route_network = computations.generate_route_network(stop_nodes, maximum_walking_distance, number_of_generations)
    snapped_route_network = snap_route_network_to_road(route_network)

    return JsonResponse({'route_network': dumps(snapped_route_network)})
