from __future__ import absolute_import

import math
import random


# Decide which functions belong to utils.py

def generate_route_network(stop_nodes, max_walking_dist, num_generations):
    route_network = {}
    for i in range(num_generations):
        route_network[i] = generate_route(stop_nodes, max_walking_dist, i)

    return route_network


def generate_route(stop_nodes, max_walking_dist, route_id):
    enable_stop_nodes(stop_nodes)



    route = []
    selected_node = random.choice(stop_nodes)

    stop_node_coordinates = [n.coordinates for n in stop_nodes]
    stop_nodes_kd_tree = None

    while not all_nodes_disabled(stop_nodes):
        route.append(selected_node)
        enabled_surrounding_nodes = get_enabled_surrounding_nodes(stop_nodes, stop_nodes_kd_tree,
                                                                  selected_node, max_walking_dist)

        selected_node = get_surrounding_node_with_highest_edge_probability(selected_node, enabled_surrounding_nodes)

    return route


def enable_stop_nodes(stop_nodes):
    for n in stop_nodes:
        n.enable()


def all_nodes_disabled(stop_nodes):
    return get_num_disabled(stop_nodes) == 0


def get_num_disabled(stop_nodes):
    return sum(1 for n in stop_nodes if not n.enabled)


def get_enabled_surrounding_nodes(stop_nodes, node_kd_tree, source_node, radius):
    surrounding_nodes_indices = node_kd_tree.query_ball_point(
        source_node, radius - 0.00000000000000000000000000001
    )

    return [stop_nodes[i] for i in surrounding_nodes_indices if stop_nodes[i].enabled]


def get_surrounding_node_with_highest_edge_probability(source_node, surrounding_nodes):
    highest_edge_prob = 0
    highest_edge_prob_node = None

    for n in surrounding_nodes:
        edge_prob = get_edge_probability(source_node, n, len(surrounding_nodes))
        if edge_prob > highest_edge_prob:
            highest_edge_prob = edge_prob
            highest_edge_prob_node = n

    return highest_edge_prob_node


def get_edge_probability(source, destination, normalization_factor):
    return math.exp(-(euclidean(source, destination))) / float(normalization_factor)


# TODO: Check if you can use scipy.spatial.distance.euclidean instead
def euclidean(x, y):
    sum_squared = 0.0
    for i in range(len(x)):
        sum_squared += (x[i] - y[i]) ** 2

    return sum_squared ** 0.5
