# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import networkx as nx
from preprocessor.utils import get_location_road_graph
from stopgenerator.utils import closest_node
from scipy.spatial.distance import euclidean
import ast
import logging
# logging.basicConfig(filename='routegenerator_utils.log', level=logging.DEBUG, format = '%(asctime)s:%(name)s:%(message)s')
from loggerinitializer import initialize_logger

road_data = None

initialize_logger('','utils')

def get_location_road_nodes():
    logging.info("RETRIEVING LOCATION ROAD NODES")
    if road_data == None:
        location_road_graph = get_location_road_graph()
        global road_data
        road_data = [RoadNode(data) for node, data in location_road_graph.nodes_iter(data=True)]

    logging.info("RETURNING ")
    return road_data

def snap_route_network_to_road(route_network):
    logging.info("Initalizing Snap Route Network to Road")
    logging.debug(route_network)
    logging.info("Retrieving Graph")
    location_road_graph = get_location_road_graph()
    logging.info("Acquiring Road Node Data")
    location_road_nodes = [RoadNode(data) for node, data in location_road_graph.nodes_iter(data=True)]
    snapped_route_network = []
    list_graphs = []
    route_id = 0
    logging.info("Starting Snapping per Route Loop")
    for route in route_network:
        logging.info("Snapping")
        snapped_route = snap_route_to_road(location_road_graph, location_road_nodes, route)
        logging.info("Setting Edge Attributes of Route ID: " + str(route_id))
        nx.set_edge_attributes(snapped_route, 'route_id', route_id)
        route_id = route_id + 1
        logging.info("Current Route Status")
        logging.debug(snapped_route.nodes(data=True))
        logging.debug(snapped_route.edges(data=True))
        logging.info("Adding Nodes to Graph")
        # snapped_route_new = add_node_coords_to_coordinate_list_graph(snapped_route)
        to_snap = snapped_route
        logging.info("Adding Distance to Graph")
        snapped_route = add_distance_to_graph(to_snap)
        logging.debug(snapped_route.nodes(data=True))
        logging.debug(snapped_route.edges(data=True))
        logging.info("Appending")
        list_graphs.append(snapped_route)
        logging.info("Appended")

        logging.info("Snapping Edges")
        snapped_edges = list(snapped_route.edges_iter(data='road_path', default=1))

        snapped_route = []
        logging.info("Edges Snapped")
        for e in snapped_edges:
            logging.info("Appending Snapped Route")
            logging.debug(e)
            snapped_route.append(convert_uuid_route(location_road_nodes, e[2]))
            logging.info("Appended Snapped Route")

        # Flatten list of UUID edges
        # snapped_route = [e for snapped_edges in snapped_route for e in snapped_edges]
        snapped_route = connect_snapped_edges(snapped_route)
        snapped_route_network.append(snapped_route)

    logging.info("MERGE")
    graph = merge_list_graphs(list_graphs)

    logging.debug("MERGED GRAPH")
    logging.debug(graph.nodes(data=True))
    logging.debug(graph.edges(data=True))


    list_graphs_to_string = prepare_graph_for_export_string(graph)
    # snapped_route_network = convert_list_graph_to_list_route_coordinates(list_graphs)
    return snapped_route_network, list_graphs_to_string, list_graphs

def convert_list_graph_to_list_route_coordinates(list_graphs):
    route_net = []
    for route in list_graphs:
        for u,v,d in route.edges(data='lat_long_road_path'):
            route_net.append(d)
    logging.info("Route Network Coordinate List")
    logging.debug(route_net)
    return route_net


def merge_list_graphs(list_graphs):
    G = nx.Graph()
    for graphs in list_graphs:
        G = nx.compose(graphs,G)
    return G



def get_max_route_in_graph(graph):
    max_route = 0
    for i in graph.edges(data='route_id'):
        print i[2]
        if max_route < i[2]:
            max_route = i[2]
    return max_route


def convert_to_list_graph(graph):
    logging.info("Converting Graph to Graph List")
    list_graph = []
    max_route = get_max_route_in_graph(graph)

    list_temp_nodes_in_edges = []
    for i in range(0,max_route):
        G = nx.Graph()
        for e in graph.edges(data=True):
            if graph.get_edge_data(*e)["route_id"] == i :
                G.add_edge(*e)
                list_temp_nodes_in_edges.append(e[0])
                list_temp_nodes_in_edges.append(e[1])
        list_temp_nodes_in_edges = list(set(list_temp_nodes_in_edges))
        print (list_temp_nodes_in_edges)
        for n in graph.nodes(data = True):
            if n[0] in list_temp_nodes_in_edges:
                G.add_node(*n)
        print("Route" + str(i))
        print(G.nodes(data=True))
        print(G.edges(data=True))
        list_graph.append(G)
    return list_graph




def prepare_graph_from_import(input, type):
    graph = nx.Graph()
    string_input = None
    if type == 'f':
        string_input = open(input, 'r', encoding="utf-8-sig").read()
    elif type == 's':
        string_input = input

    string_input = string_input.split("\n")
    flag = False
    for line in string_input:
        line = line.strip('(')
        line = line.strip(')')
        if (flag == False):
            if (line == "|"):
                flag = True
            else:
                elem = line.split(", ")
                node_id = int(elem[0])
                temp_dict_str = elem[1] + ", " + elem[2]
                temp_dict = ast.literal_eval(temp_dict_str)
                graph.add_node(node_id, temp_dict)
        elif (flag == True):
            elem = line.split("{")
            node_id = elem[0].split(",")

            if (node_id[0] != "" and node_id != ""):
                node_id_1 = int(node_id[0])
                node_id_2 = int(node_id[1])

                temp_dict_str = "{" + elem[1]
                temp_dict = ast.literal_eval(temp_dict_str)
                graph.add_edge(node_id_1, node_id_2, temp_dict)

    return graph

def prepare_graph_for_export_string(graph):
    location_road_nodes = get_location_road_nodes()
    export_graph = nx.Graph()
    snapped_edges = list(graph.edges_iter(data='road_path', default=1))
    for v, inner_d in graph.nodes(data=True):
        export_graph.add_node(v, inner_d)

    i = 0
    for edge in graph.edges_iter(data=True):
        temp_dict = {}
        temp_dict["route_id"] = edge[2]["route_id"]
        temp_dict["road_path"] = edge[2]["road_path"]

        latlng_list = []
        if(len(snapped_edges[i][2]) > 0):
            for elem in convert_uuid_route(location_road_nodes, snapped_edges[i][2]):
                latlng_list.append(elem.latlng)
            temp_dict["lat_long_road_path"] = latlng_list
            temp_dict["distance"] = get_total_distance_intersections(latlng_list)
            export_graph.add_edge(edge[0],edge[1],temp_dict)

        i = i + 1


    str_graph_output = ""
    for v, inner_d in export_graph.nodes(data=True):
        str_graph_output =  str_graph_output + "(" + str(v) + ", " + str(inner_d) + ")\n"

    str_graph_output = str_graph_output + "|\n"
    for edge in export_graph.edges_iter(data=True):
        str_graph_output = str_graph_output + str(edge) +"\n"

    return str_graph_output

def add_distance_to_graph(graph):
    logging.info("Entered Adding Distance to Graph")
    logging.debug(graph.nodes(data=True))
    logging.debug(graph.edges(data=True))
    location_road_nodes = get_location_road_nodes()
    logging.info("Retrieved Road Nodes")
    export_graph = nx.Graph()
    logging.info("Initalized Graph")
    snapped_edges = list(graph.edges_iter(data='road_path', default=1))
    logging.debug("Snapped Edges: {}".format(snapped_edges))
    dict_temp_tup = {}

    for v, inner_d in graph.nodes(data=True):
        tup = [inner_d['lat'], inner_d['lon']]
        dict_temp_tup[v] = tup
        export_graph.add_node(v, inner_d)

    i = 0
    for edge in graph.edges_iter(data=True):
        temp_dict = {}
        temp_dict["route_id"] = edge[2]["route_id"]
        temp_dict["road_path"] = edge[2]["road_path"]

        latlng_list = []
        if(len(snapped_edges[i][2]) > 0):
            for elem in convert_uuid_route(location_road_nodes, snapped_edges[i][2]):
                latlng_list.append(elem.latlng)
            temp_lat_lng_list = latlng_list
            latlng_list = [dict_temp_tup[edge[0]]] + temp_lat_lng_list + [dict_temp_tup[edge[1]]]
            temp_dict["lat_long_road_path"] = latlng_list
            temp_dict["distance"] = get_total_distance_intersections(latlng_list)
            export_graph.add_edge(edge[0],edge[1],temp_dict)

        i = i + 1
    return export_graph

def get_total_distance_intersections(latlng_list):
    distance = 0.0
    flag = False
    prev_latlng = [0,0]
    for latlng in latlng_list:
        if not flag:
            prev_latlng = latlng
            flag = True
        else:
            distance = distance + euclidean(prev_latlng, latlng)
            prev_latlng = latlng

    return distance * 111000

def connect_snapped_edges(snapped_edges):
    connected_edge = []

    while len(snapped_edges) > 0:
        curr_edge = []
        curr_edge = consecutive_connect(curr_edge, snapped_edges.pop(0))

        for e in snapped_edges:
            consecutive_edge = consecutive_connect(curr_edge, e)
            if consecutive_edge is not None:
                curr_edge = consecutive_edge
                snapped_edges.remove(e)

        new_connected_edge = consecutive_connect(connected_edge, curr_edge)
        connected_edge = new_connected_edge if new_connected_edge is not None else connected_edge

    return connected_edge


def consecutive_connect(e1, e2):
    if len(e1) == 0:
        return e2
    elif len(e2) == 0:
        return e1

    if e1[len(e1) - 1] == e2[0]:
        return e1 + e2
    elif e2[len(e2) - 1] == e1[0]:
        return e2 + e1
    else:
        return None


def snap_route_to_road(location_road_graph, location_road_nodes, route_stop_nodes):
    snapped_route = nx.Graph()
    snapped_route.add_node(route_stop_nodes[0].uuid)

    # Add UUID of all stop nodes as nodes in the graph
    for n in route_stop_nodes:
        snapped_route.add_node(n.uuid, lat=n.latlng[0], lon=n.latlng[1])

    # Add the shortest path for each consecutive node as an edge in the graph
    for i in range(len(route_stop_nodes) - 1):
        source_node = route_stop_nodes[i]
        dest_node = route_stop_nodes[i + 1]
        shortest_road_path = get_shortest_road_path(location_road_graph, location_road_nodes, source_node, dest_node)
        snapped_route.add_edge(source_node.uuid, dest_node.uuid, road_path=shortest_road_path)
    return snapped_route


def get_shortest_road_path(location_road_graph, location_road_nodes, source_stop_node, dest_stop_node):
    closest_road_node_to_source = closest_node(location_road_nodes, source_stop_node)
    closest_road_node_to_dest = closest_node(location_road_nodes, dest_stop_node)

    if nx.has_path(location_road_graph, closest_road_node_to_source.uuid, closest_road_node_to_dest.uuid):
        return nx.shortest_path(location_road_graph, closest_road_node_to_source.uuid, closest_road_node_to_dest.uuid)
    else:
        return {}


def convert_uuid_route(nodes, uuid_route):
    return [get_node_with_uuid(nodes, uuid) for uuid in uuid_route]


def get_node_with_uuid(nodes, uuid):
    for n in nodes:
        if n.uuid == uuid:
            return n

    return None


class RoadNode(object):
    def __init__(self, data):
        self.uuid = data['osmid']
        self.latlng = [data['y'], data['x']]
