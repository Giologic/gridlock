# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from stopgenerator.utils import convert_latlng_to_stop_nodes
from routegenerator.utils import snap_route_network_to_road
from .computations import perform_genetic_algorithm, compute_fitness_score


@csrf_exempt
def check_fitness_score(request):
    route_network = json.loads(request.POST['route_network_coordinates'])
    route_network = [convert_latlng_to_stop_nodes(r) for r in route_network]

    snapped_route_network = snap_route_network_to_road(route_network, output_graph=True, location_road_graph=None)

    num_failure_removal = int(request.POST['num_failure_removal'])
    weight_random_failure = float(request.POST['weight_random_failure'])
    weight_targeted_failure = float(request.POST['weight_targeted_failure'])
    weight_radius_of_gyration = float(request.POST['weight_radius_of_gyration'])

    fitness_score = compute_fitness_score(snapped_route_network, num_failure_removal,
                                          weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)

    return JsonResponse({'fitness_score': fitness_score})
