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

    print(snapped_route_network.edges(data=True))

    num_failure_removal = int(request.POST['num_failure_removal'])
    weight_random_failure = float(request.POST['weight_random_failure'])
    weight_targeted_failure = float(request.POST['weight_targeted_failure'])
    weight_radius_of_gyration = float(request.POST['weight_radius_of_gyration'])

    fitness_score = compute_fitness_score(snapped_route_network, num_failure_removal,
                                          weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)

    return JsonResponse({'fitness_score': fitness_score})


@csrf_exempt
def optimize_route_network(request):
    stop_node_coordinates = json.loads(request.POST['stop_node_coordinates'])
    stop_nodes = convert_latlng_to_stop_nodes(stop_node_coordinates)

    route_network = json.loads(request.POST['route_network_coordinates'])
    route_network = [convert_latlng_to_stop_nodes(r) for r in route_network]
    snapped_route_network = snap_route_network_to_road(route_network, output_graph=True, location_road_graph=None)

    print(snapped_route_network.nodes(data=True))

    # max_walking_dist = float(request.POST['max_walking_dist'])
    #
    # num_failure_removal = int(request.POST['num_failure_removal'])
    # weight_random_failure = float(request.POST['weight_random_failure'])
    # weight_targeted_failure = float(request.POST['weight_targeted_failure'])
    # weight_radius_of_gyration = float(request.POST['weight_radius_of_gyration'])
    #
    # num_evolutions = int(request.POST['num_evolutions'])
    # route_mutation_probabilities = [0.7, 0.2, 0.1, 0.1]
    #
    # num_generated_network_mutations_per_evolution = int(request.POST['num_mutations_per_evolution'])
    # optimized_route_network = perform_genetic_algorithm(stop_nodes, snapped_route_network, max_walking_dist,
    #                                                     num_evolutions, num_generated_network_mutations_per_evolution,
    #                                                     route_mutation_probabilities, num_failure_removal,
    #                                                     weight_random_failure,
    #                                                     weight_targeted_failure, weight_radius_of_gyration)
    #
    # new_fitness_score = compute_fitness_score(optimized_route_network, num_failure_removal,
    #                                           weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)
    #
    # return JsonResponse({'new_fitness_score': new_fitness_score})
