# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import computations
import json
import logging
logging.basicConfig(filename='routegenerator_views.log', level=logging.DEBUG, format = '%(asctime)s:%(name)s:%(message)s')

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
    snapped_route_network, export_string, list_graphs = snap_route_network_to_road(route_network)
    logging.debug('Snapped Route Network : {}'.format(snapped_route_network))
    logging.debug('Export String : {}'.format(export_string))
    logging.debug('List Graphs : {}'.format(list_graphs))

    # print(type(export_string))
    # print(export_string)
    return JsonResponse({'route_network': dumps(snapped_route_network), 'export_string': export_string})
