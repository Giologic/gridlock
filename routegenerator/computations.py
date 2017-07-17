from __future__ import absolute_import, division

import math
import random
import logging

from scipy.spatial import KDTree
from scipy.spatial.distance import euclidean
from stopgenerator.utils import all_nodes_disabled, enable_stop_nodes

from loggerinitializer import initialize_logger

initialize_logger('','computations')

def generate_route_network(stop_nodes, max_walking_dist, num_generations):
    # k-dimensional tree is built only once per route for optimization
    stop_node_coordinates = [n.latlng for n in stop_nodes]
    stop_nodes_kd_tree = KDTree(stop_node_coordinates)
    possible_start_nodes = [x for x in stop_nodes]

    route_network = []
    for i in range(num_generations):
        route_network.append(generate_route(stop_nodes, possible_start_nodes, stop_nodes_kd_tree, max_walking_dist))

    return route_network


def generate_route(stop_nodes, possible_start_nodes, stop_nodes_kd_tree, max_walking_dist):
    route = []
    enable_stop_nodes(stop_nodes)
    selected_node = random.choice(possible_start_nodes)
    possible_start_nodes.remove(selected_node)

    while not all_nodes_disabled(stop_nodes):
        route.append(selected_node)
        disable_surrounding_nodes(stop_nodes, stop_nodes_kd_tree, selected_node, max_walking_dist / 111111)
        enabled_nodes = [n for n in stop_nodes if n.enabled]
        selected_node = get_enabled_node_with_highest_edge_probability(selected_node, enabled_nodes)

    return route


def disable_surrounding_nodes(stop_nodes, stop_nodes_kd_tree, source_node, radius):
    surrounding_node_indices = stop_nodes_kd_tree.query_ball_point(source_node.latlng,
                                                                   radius - 0.00000000000000000000000000001)
    for i in surrounding_node_indices:
        stop_nodes[i].enabled = False


def get_enabled_node_with_highest_edge_probability(source_node, enabled_nodes):
    highest_edge_prob = 0
    highest_edge_prob_node = None

    for n in enabled_nodes:
        edge_prob = get_edge_probability(source_node, n, len(enabled_nodes))
        if edge_prob > highest_edge_prob:
            highest_edge_prob = edge_prob
            highest_edge_prob_node = n

    return highest_edge_prob_node


def get_edge_probability(source, destination, normalization_factor):
    return math.exp(-(euclidean(source.latlng, destination.latlng))) / float(normalization_factor)
