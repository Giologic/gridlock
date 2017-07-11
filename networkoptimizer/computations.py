from __future__ import unicode_literals, division

import networkx as nx
import numpy as np
import random
from loggerinitializer import *
from preprocessor.utils import get_location_road_graph
from routegenerator.computations import generate_route_network
from routegenerator.utils import snap_route_network_to_road, prepare_graph_for_export, create_graph_from_route_network


initialize_logger('')

logging.debug("debug message")
logging.info("info message")
logging.warning("warning message")
logging.error("error message")
logging.critical("critical message")

import logging

logging.basicConfig(filename="Log_Test_File.txt",
                level=logging.DEBUG,
                format='%(levelname)s: %(asctime)s %(message)s',
                datefmt='%m/%d/%Y %I:%M:%S')


def export_list_score(list_score):
    with open("scores.txt", "w") as output:
        output.write(str(list_score))


def perform_genetic_algorithm(stop_nodes, road_snapped_network_graph,
                              max_walking_dist, num_evolutions, num_generated_network_mutations_per_evolution,
                              route_mutation_probabilities,
                              num_failure_removal, weight_random_failure, weight_targeted_failure, weight_gyration, num_random_values, weight):
    # (maxnumberofnodes)! / 2! (maxnumberofnodes - 2)!
    logging.info("Genetic Algorithm Init")
    logging.debug("stop_nodes" + str(stop_nodes))
    logging.debug("graph_nodes" + str(road_snapped_network_graph.nodes(data=True)))
    logging.debug("edge_nodes" + str(road_snapped_network_graph.edges(data=True)))
    logging.debug("max_walking_dist" + str(max_walking_dist))
    logging.debug("num_evolutions" + str(num_evolutions))
    logging.debug("num_generated_network_mutations_per_evolution" + str(num_generated_network_mutations_per_evolution))
    logging.debug("route_mutation_probabilities" + str(route_mutation_probabilities))
    logging.debug("num_failure_removal" + str(num_failure_removal))
    logging.debug("weight_random_failure" + str(weight_random_failure))
    logging.debug("weight_targeted_failure" + str(weight_targeted_failure))
    logging.debug("weight_gyration" + str(weight_gyration))


    location_road_graph = get_location_road_graph()
    list_scores = []
    logging.info("Starting Evolution Loop")
    for i in range(num_evolutions):
        logging.debug("Evolution Loop @ " + str(i))
        num_mutations = np.random.choice(len(route_mutation_probabilities), 1, route_mutation_probabilities)[0]
        logging.debug("num_mutations @ " + str(i) + "=" + str(num_mutations))
        mutations = []
        if num_mutations > 0:
            for j in range(num_generated_network_mutations_per_evolution):
                logging.info("Mutation Loop @ " + str(j))
                # if num_mutations > 0 then randomly select n (which is ALSO EQUAL to num_mutations)
                #  routes to be replaced by a new route
                # replace the routes with the newly generated routes
                # append the modified network to the mutations list

                mutation_route_network = road_snapped_network_graph
                logging.info("MUTATION ROUTE NETWORK")
                logging.debug(str(mutation_route_network.nodes(data=True)))
                logging.debug(str(mutation_route_network.nodes(data=True)))
                new_route_network = create_graph_from_route_network(generate_route_network(stop_nodes, max_walking_dist, num_mutations))
                logging.info("NEW ROUTE NETWORK")
                logging.debug(str(new_route_network.nodes(data=True)))
                logging.debug(str(new_route_network.edges(data=True)))
                # routes_to_replace = random.sample(range(len(num_route_gen)), num_mutations)
                logging.info("ROUTES TO REPLACE")
                routes_to_replace = random.sample(range(10), num_mutations)
                logging.info("MUTATED GRAPH")
                mutated_graph = replace_routes(mutation_route_network, routes_to_replace, new_route_network)
                logging.debug(str(mutated_graph.nodes(data=True)))
                logging.debug(str(mutated_graph.edges(data=True)))
                # print("MUTATION: " + j)
                mutations.append(mutated_graph)
                logging.info("APPENDING MUTATED GRAPH")
                logging.debug(str(mutated_graph.nodes(data=True)))
                logging.debug(str(mutated_graph.nodes(data=True)))

                # mutation_route_network = snap_route_network_to_road(mutation_route_network, output_graph=True,
                #                                                                     location_road_graph=location_road_graph)


        # pick the highest scoring mutation among the num_generated_network_mutations_per_evolution
        # mutations.append(snap_route_network_to_road(road_snapped_network, output_graph=True))
        if len(mutations) > 0:
            road_snapped_network_graph, score = get_highest_scoring_mutation(mutations, num_random_values, weight)
            list_scores.append(score)

    export_list_score(list_scores)
    prepare_graph_for_export(road_snapped_network_graph, get_location_road_graph)
    return road_snapped_network_graph


def replace_routes(graph, routes_to_replace, generated_graph):
    logging.info("INIT REPLACE ROUTES:" )
    logging.debug("graph" + str(graph))
    logging.debug("routes_to_replace" + str(routes_to_replace))
    logging.debug("generated_graph" + str(generated_graph))
    i = 0

    logging.info("INIT REPLACE ROUTES LOOP EDGES")
    for e in graph.edges(data="route_id"):
        if (graph.get_edge_data(*e)["route_id"] in routes_to_replace):
            logging.debug("REMOVING" + str(graph.get_edge_data(*e)))
            graph.remove_edge(*e[:2])
            #         e in generated_graph.edges(data="route_id")
            #         if(generated_graph.get_edge_data(*e)["route_id"] == i)
            #             u,v,d
            for u, v, d in generated_graph.edges(data=True):
                if (d['route_id'] == i):
                    d['route_id'] = routes_to_replace[i]
                    logging.debug("PLACING NEW EDGE TO " + str(routes_to_replace[i]))
                    graph.add_edge(u, v, d)
            i = i + 1

    return graph


def get_highest_scoring_mutation(mutations, num_random_values, weight):
    highest_scoring_graph = nx.Graph()
    highest_score = 0.0
    for graph in mutations:
        computed_score = compute_fitness_score(graph, num_random_values, weight)
        if (computed_score > highest_score):
            highest_scoring_graph = graph
            highest_score = computed_score

    return highest_scoring_graph, highest_score


def _get_total_weighted_distance(graph, weight):
    dp = _get_distance_individual(graph)
    w = weight
    total_weighted_distance = 0.0
    T = {}
    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                g = get_nodes_shortest_path(shortest_path_nodes, graph)
                T = _get_no_of_transfers(g)
                a = 1.0
            elif not nx.has_path(graph, k_x, k_y):
                a = 10.0

            b = float(dp[(str(k_x), str(k_y))])
            weighted_distance = a * b + (w * T)
            total_weighted_distance = float(total_weighted_distance) + float(weighted_distance)

    return total_weighted_distance


def _get_distance_individual(graph):
    T = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                accumulated_distance = 0.0
                if (len(shortest_path_nodes) > 1):
                    for i in range(0, len(shortest_path_nodes) - 1):
                        edge_distance = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('distance')
                        print(accumulated_distance)
                        accumulated_distance = float(accumulated_distance) + float(edge_distance)
                    T[(str(k_x), str(k_y))] = accumulated_distance
                else:
                    T[(str(k_x), str(k_y))] = 0
            else:
                T[(str(k_x), str(k_y))] = 0

    return T


def get_nodes_shortest_path(shortest_path_nodes, graph):
    new_graph = nx.Graph()

    for k_y, v_y in graph.nodes_iter(data=True):
        for elem in shortest_path_nodes:
            if elem == k_y:
                new_graph.add_node(k_y, lat=v_y.get('lat'), lon=v_y.get('lon'), route_id=v_y.get('route_id'))

                #     print (graph.nodes(data=True))

    return graph


def _get_no_of_transfers(graph):
    temp = []
    p = graph.copy()
    no_of_tranfer = 0
    #     print ("PATH")
    #     print(p.nodes(data=True))

    for k_y, v_y in p.nodes_iter(data=True):
        if (len(p.nodes()) > 1):
            if str(v_y.get("route_id")) not in temp:
                temp.append(str(v_y.get("route_id")))
            no_of_transfer = len(temp) - 1
        else:
            no_of_tranfer = 0

    return no_of_tranfer


def compute_fitness_score(road_snapped_network_graph, num_random_values, weight):
    # robustness failure
    # robustness targeted
    return compute_radius_of_gyration(road_snapped_network_graph, num_random_values, weight)


def compute_radius_of_gyration(road_snapped_network_graph, num_random_values, weight):
    return _get_efficiency_sum(road_snapped_network_graph, num_random_values, weight)


def _get_efficiency_sum(graph, no_of_random_values, weight):
    efficiency_sum = 0.0
    weighted_list = _get_yweighted_list(graph, weight)

    efficiency_sum_list = random.sample(weighted_list.keys(), no_of_random_values)
    for k_x, k_y in efficiency_sum_list:
        temp = weighted_list[(str(k_x), str(k_y))]
        efficiency_sum = float(temp) + float(efficiency_sum)

    return efficiency_sum


def _get_yweighted_list(graph, weight):
    dp = _get_distance_individual(graph)
    dw = _get_total_weighted_distance(graph, weight)
    Y = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                Y[(str(k_x), str(k_y))] = float(dp[(str(k_x), str(k_y))]) / float(dw)
            else:
                Y[(str(k_x), str(k_y))] = 0.0

    return Y
