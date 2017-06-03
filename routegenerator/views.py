# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import computations
import json
from json_tricks import dumps

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from stopgenerator.utils import convert_latlng_to_stop_nodes


@csrf_exempt
def generate_route_network(request):
    stop_node_coordinates = json.loads(request.POST['stop_node_coordinates'])
    stop_nodes = convert_latlng_to_stop_nodes(stop_node_coordinates)
    route_network = computations.generate_route_network(stop_nodes, 350, 10)

    return JsonResponse({'route_network': dumps(route_network)})
