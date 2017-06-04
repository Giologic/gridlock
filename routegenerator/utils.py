# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import networkx as nx

from preprocessor.utils import get_location_road_graph
from stopgenerator.utils import closest_node


def snap_route_network_to_road(route_network):
    location_road_graph = get_location_road_graph()
    location_road_nodes = [RoadNode(data) for node, data in location_road_graph.nodes_iter(data=True)]
    snapped_route_network = nx.Graph()

    for route in route_network:
        snapped_route = snap_route_to_road(location_road_graph, location_road_nodes, route)
        snapped_route_network = nx.compose(snapped_route_network, snapped_route)

    snapped_route_network = list(snapped_route_network.edges_iter(data='road_path', default=1))
    snapped_route_network = convert_uuid_routes(location_road_nodes, [x[2] for x in snapped_route_network])
    return snapped_route_network


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


def convert_uuid_routes(nodes, network_uuid_routes):
    routes = []
    for uiid_route in network_uuid_routes:
        routes.append([get_node_with_uuid(nodes, uuid) for uuid in uiid_route])

    return routes


def get_node_with_uuid(nodes, uuid):
    for n in nodes:
        if n.uuid == uuid:
            return n

    return None


class RoadNode(object):
    def __init__(self, data):
        self.uuid = data['osmid']
        self.latlng = [data['y'], data['x']]
