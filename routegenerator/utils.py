# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import networkx as nx

from preprocessor.utils import get_location_road_graph
from stopgenerator.utils import closest_node


def snap_route_network_to_road(route_network):
    location_road_graph = get_location_road_graph()
    location_road_nodes = [RoadNode(data) for node, data in location_road_graph.nodes_iter(data=True)]
    snapped_route_network = []

    for route in route_network:
        snapped_route = snap_route_to_road(location_road_graph, location_road_nodes, route)
        snapped_edges = list(snapped_route.edges_iter(data='road_path', default=1))

        snapped_route = []
        for e in snapped_edges:
            snapped_route.append(convert_uuid_route(location_road_nodes, e[2]))

        # Flatten list of UUID edges
        # snapped_route = [e for snapped_edges in snapped_route for e in snapped_edges]
        snapped_route = connect_snapped_edges(snapped_route)
        snapped_route_network.append(snapped_route)

    return snapped_route_network


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
