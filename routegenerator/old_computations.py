from __future__ import absolute_import
import random
import numpy as np
import scipy.spatial as spatial
import math
from . import old_node, old_utils
import networkx as nx

def generate_network(generated_nodes,distance_unit,number_generations):
    network = {}


    counter = 0
    # print(generated_nodes[2]._node_id)
    while(counter < number_generations):

        counter += 1
        print("Generation: " + str(counter))
        route = generate_route(generated_nodes, distance_unit, counter)
        # print(route)
        network[counter] = route
        _reset_node_status(generated_nodes)


    return network



def generate_route(generated_nodes,distance_unit, route_id):

    route = []
    # if 1st iter get rand as source node
    # else get selected node as source node
    # get closest distance from the source node
    # generate probability table
    # node with highest probability becomes added to the list of route nodes and the new selected source node
    # disable all previously nominated nodes including the previously selected node
    # ITERATE


    # print(generated_nodes[0])
    # print(generated_nodes)
    flag = True
    randNum = random.randrange(0, len(generated_nodes) - 1)
    source_node = generated_nodes[randNum]
    while flag:
        source_node.route_id = route_id
        route.append(source_node)

        highest_prob, generated_nodes = _get_edge_probability_from_surrounding_nodes(source_node, generated_nodes, distance_unit)
        # print(highest_prob[0],highest_prob[1])

        if (getNumDisabled(generated_nodes) != len(generated_nodes)):
            source_node = highest_prob[0]

        # print("NUM DIS" + str(getNumDisabled(generated_nodes)))

        if(getNumDisabled(generated_nodes) == len(generated_nodes)):
            flag = False

    return route

def _find_surrounding_nodes(point, generated_nodes, distance_unit):
    distance_unit = distance_unit/111111

    point = point.coordinates
    points = np.array(old_utils.convert_to_xy_list(generated_nodes))
    point_tree = spatial.cKDTree(points)
    # This finds the index of all points within distance distance_unit of point (x,y).
    # print("DIST UNIT: " + str(distance_unit))
    disclude_array = point_tree.query_ball_point(point, distance_unit - 0.00000000000000000000000000001)

    #convert to dictionary
    disclude_array_dict = {}
    for elements in disclude_array:
        disclude_array_dict[str(elements)] = elements

    #iterate to determine possible nodes
    possible_index_list = []
    disabled_index_list = []
    for i in range(len(points)):
        if str(i) not in disclude_array_dict.keys() and generated_nodes[i]._status == old_node.is_enabled():
            possible_index_list.append(i)
        else:
            generated_nodes[i].disable()
            # print("DISABLE")
            # print(generated_nodes[i].coordinates)
            # print(generated_nodes[i]._status)
            # print("++")

    return possible_index_list, generated_nodes

def _get_edge_probability_from_surrounding_nodes(source, generated_nodes, distance_unit):

    possible_index_list, newly_generated_nodes = _find_surrounding_nodes(source, generated_nodes, distance_unit)

    map = old_utils.convert_indices_to_node_list(possible_index_list, newly_generated_nodes)
    isInit = True
    problist = []
    highestprob = None

    for cell in map:
        edgeProb = _get_edge_probability(source.coordinates, cell.coordinates, len(map))
        # problist.append((node.Node((cell).coordinates), _get_edge_probability(source.coordinates, cell.coordinates, len(generated_nodes) - getNumDisabled(generated_nodes))))
        if(isInit):
            highestprob = [cell,edgeProb]
            isInit = False
        else:
            if(edgeProb > highestprob[1]): highestprob = [cell,edgeProb]

    return highestprob, newly_generated_nodes

def _get_edge_probability(source, destination, normalization_factor):
    return math.exp(-(old_utils.euclidean(source, destination))) / float(normalization_factor)


def __match_indices_to_matrix(index_list, map):
    possible_nodes_map = []
    for indices in index_list:
        possible_nodes_map.append(map[indices])

    return possible_nodes_map

def _disable_nodes(node_list):
    new_node_list = []
    for node_element in node_list:
        node_element.disable()
    return new_node_list

def _reset_node_status(node_list):
    new_node_list = []
    for node_element in node_list:
        node_element.enable()
    return new_node_list

def getNumDisabled(node_matrix):
    accumulator = 0
    for cell in node_matrix:

        if cell._status == (old_node.is_disabled() or old_node.is_eliminated()):
            accumulator = accumulator + 1

    return accumulator

def create_road_snapped_network(map_graph, network):
    network_graph = nx.Graph()
    ctr = 0

    for nodelist in network:
        ctr = ctr + 1
        # print(network.get(nodelist))
        network_graph = nx.compose(network_graph,__create_road_snapped_route(map_graph, network.get(nodelist)))
    return network_graph


def __create_road_snapped_route(map_graph, node_list):
    route_graph = nx.Graph()
    # print(len(node_list))
    for i in range(0,len(node_list) - 1):
        print("Path[" + str(i) + "]:    ")
        #source stop coordinate
        source = node_list[i]
        #source stop coordinate
        dest = node_list[i+1]

        if(i == 0):
            route_graph.add_node(source.node_id, lat=source.coordinates[0], lon=source.coordinates[1], route_id = source.route_id)
        route_graph.add_node(dest.node_id, lat=dest.coordinates[0], lon=source.coordinates[1], route_id = dest.route_id)
        #get shortest path road intersections
        # shortest_path = utils.get_shortest_path_line_string(map_graph, source.coordinates,dest.coordinates)
        shortest_path = old_utils.get_shortest_path_line_string_local(map_graph, source.coordinates, dest.coordinates)
        #create edges with distance attribute and list of intersections used from source stop to dest stop
        # graph = nx.compose(new_graph,utils.create_graph_from_osm_coordinates(map_graph,shortest_path))
        route_graph.add_edge(source.node_id,dest.node_id,intersections = shortest_path, dist = old_utils.get_total_distance_intersections(map_graph,source.coordinates,dest.coordinates,shortest_path))
        # route_graph.add_edge(source.node_id,dest.node_id, dist = utils.get_total_distance_intersections(map_graph,source.coordinates,dest.coordinates,shortest_path))

    return route_graph


