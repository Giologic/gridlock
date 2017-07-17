# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from stopgenerator.utils import convert_latlng_to_stop_nodes
from routegenerator.utils import snap_route_network_to_road, convert_to_list_graph
from .computations import perform_genetic_algorithm, compute_fitness_score
import networkx as nx
import logging

from loggerinitializer import initialize_logger

initialize_logger('','views')

@csrf_exempt
def check_fitness_score(request):
    # route_network = json.loads(request.POST['route_graph'])
    # route_network = convert_to_list_graph(deserialize("route_graph.txt"))
    snapped_route_network = nx.read_yaml(route_network.yaml)
    # snapped_route_network = convert_to_list_graph(route_network)

    # route_network = [convert_latlng_to_stop_nodes(r) for r in route_network]
    # snapped_route_network = snap_route_network_to_road(route_network, output_graph=True, location_road_graph=None)

    # print(snapped_route_network.edges(data=True))

    num_failure_removal = int(request.POST['num_failure_removal'])
    # num_failure_removal = 1
    weight_random_failure = float(request.POST['weight_random_failure'])
    weight_targeted_failure = float(request.POST['weight_targeted_failure'])
    weight_radius_of_gyration = float(request.POST['weight_radius_of_gyration'])

    fitness_score = compute_fitness_score(snapped_route_network, num_failure_removal,
                                          weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)

    print (fitness_score)
    return JsonResponse({'fitness_score': fitness_score})


@csrf_exempt
def optimize_route_network(request):
    stop_node_coordinates = json.loads(request.POST['stop_node_coordinates'])
    stop_nodes = convert_latlng_to_stop_nodes(stop_node_coordinates)

    logging.info("Graph Load Network")

    route_network = nx.read_yaml("route_network.yaml")
    logging.info("Route Network Nodes")
    logging.debug(route_network.nodes(data=True))
    logging.info("Route Network Edges")
    logging.debug(route_network.edges(data=True))


    snapped_route_network = convert_to_list_graph(route_network)

    ctr = 1
    for snapped in snapped_route_network:
        logging.info("Snapped Route Nodes: " + str(ctr))
        logging.debug(snapped.nodes(data=True))
        logging.info("Snapped Route Edges: " + str(ctr))
        logging.debug(snapped.edges(data=True))
        ctr = ctr + 1



    max_walking_dist = float(request.POST['max_walking_dist'])

    num_failure_removal = int(request.POST['num_failure_removal'])
    weight_random_failure = float(request.POST['weight_random_failure'])
    weight_targeted_failure = float(request.POST['weight_targeted_failure'])
    weight_radius_of_gyration = float(request.POST['weight_radius_of_gyration'])

    num_evolutions = int(request.POST['num_evolutions'])
    route_mutation_probabilities = [0.7, 0.2, 0.1, 0.1]
    num_generated_network_mutations_per_evolution = int(request.POST['num_mutations_per_evolution'])

    logging.info("Performing Genetic Algorithm")

    logging.info("@Parameters:" + "\n"
                 + "Stop Nodes: " + str(stop_nodes) + "\n"
                 + "Max Walking Distance: " + str(max_walking_dist) + "\n"
                 + "Number of Evolutions: " + str(num_evolutions) + "\n"
                 + "Number of Mutations Per Evolution: " + str(num_generated_network_mutations_per_evolution) + "\n"
                 + "Route Mutation Probabilities: " + str(route_mutation_probabilities) + "\n"
                 + "Percentage of Nodes to be Removed" + str(num_failure_removal)
                 + "Weight Random Failure: " + str(weight_random_failure) + "\n"
                 + "Weight Targeted Failure: " + str(weight_targeted_failure) + "\n"
                 + "Weight Radius of Gyration: " + str(weight_radius_of_gyration) + "\n"
                 )




    logging.info("Loaded Snapped Network")
    logging.info("Start Optimization")

    optimized_route_network = perform_genetic_algorithm(stop_nodes, snapped_route_network, max_walking_dist,
                                                        num_evolutions, num_generated_network_mutations_per_evolution,
                                                        route_mutation_probabilities, num_failure_removal,
                                                        weight_random_failure,
                                                        weight_targeted_failure, weight_radius_of_gyration)

    snapped_route_network, export_string, list_graphs = optimized_route_network
    new_fitness_score = compute_fitness_score(optimized_route_network, num_failure_removal,
                                              weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)



    return JsonResponse({'new_fitness_score': new_fitness_score, 'optimized_network':dumps(snapped_route_network), 'export_string':export_string})