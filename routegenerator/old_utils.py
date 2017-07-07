"""Utility functions for gridlock"""

from __future__ import absolute_import
from math import *
import networkx as nx
import osmnx as ox
import numpy as np

from vtown import geo
from vtown.geo.polygon import Polygon
from scipy.spatial.distance import cdist
from geopy.geocoders import Nominatim
import matplotlib.pyplot as plt



def euclidean(x, y):
    sumSq = 0.0

    # add up the squared differences
    for i in range(len(x)):
        sumSq += (x[i] - y[i]) ** 2

    # take the square root of the result
    return (sumSq ** 0.5)

def display_node(node_list):
    s="["
    ctr = 0
    for node in node_list:
        s+= node.to_string_xy()
        ctr = ctr + 1
        if(ctr < len(node_list)):
            s += ','

    s+="]"
    print(s)

def convert_to_xy_list(node_list):
    xy_list = []
    for node in node_list:
        xy_list.append(node.coordinates)

    return xy_list

def convert_indices_to_xy_list(index_list, node_list):
    new_xy_list = []
    xy_list = convert_to_xy_list(node_list)
    for indices in index_list:
        new_xy_list.append(xy_list[indices])
    return new_xy_list

def convert_indices_to_xy_list_enabled(index_list, node_list):
    new_xy_list = []
    for indices in index_list:
        if(node_list[indices].isEnabled()):
            new_xy_list.append(node_list[indices].coordinates)

    return new_xy_list

def convert_indices_to_node_list(index_list, node_list):
    new_node_list = []
    for indices in index_list:
        new_node_list.append(node_list[indices])
    return new_node_list

def display_prob_list(prob_list):
    new_node_list = []
    for cell in prob_list:
        print(str(cell[0].coordinates) +"has prob of " + str(cell[1]))

def haversine(coordinate1,coordinate2):
    lat1 = coordinate1[0]
    lat2 = coordinate2[0]
    lon1 = coordinate1[1]
    lon2 = coordinate2[1]

    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = float(sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2)
    c = float(2 * asin(sqrt(a)))
    km = float(6367 * c)
    return km

def const_km_to_unit(distance_unit):
    return (0.01/1.11) * distance_unit

def print_enabled_node_list(node_list):

    for node in node_list:
        print(str(node.coordinates) + "," + str(node.status))

def calculate_offset(coordinates, offset):


    lat = coordinates[0] + float(offset/111111)
    lon = coordinates[1] + float(offset/111111 * math.cos(lat))

    return (lat,lon)


    # Earths radius, sphere
    # R = 6378137
    #
    # #offsets in meters
    # dn = offset
    # de = offset
    #
    # #Coordinate offsets in radians
    # dLat = dn / R
    # dLon = de / (R * math.cos(math.pi * lat / 180))
    #
    # #OffsetPosition, decimal degrees
    # latO = lat + dLat * 180 / math.pi
    # lonO = lon + dLon * 180 / math.pi
    #
    # return (latO,lonO)

#
#
# def convert_network_to_networkx_graph(network):
#
#     print(network)
#     graph = nx.DiGraph()
#     for key, value in network.items():
#         prev_value = None
#         for i in range(0,len(value)):
#             print(value[i]._node_id)
#             # accumulator += 1
#
#             # print(str(accumulator) +"," + str(value[i][0]) + "," + str(value[i][1]))
#             lat = value[i].coordinates[0]
#             lon = value[i].coordinates[1]
#
#             print("PRINT" + str(lat) + "," + str(lon))
#             # g = geocoder.google([lat,lon], method='reverse')
#             geolocator = Nominatim()
#             loc = geolocator.reverse(str(lat) + "," + str(lon))
#             graph.add_node((lat,lon),
#                            name = value[i].node_id,
#                            route_id = value[i].route_id,
#                            address = loc.address
#                            )
#
#             # nx.set_node_attributes(graph,x)
#
#             # nx.draw_networkx_nodes(graph,accumulator,
#             #                        lat = value[i][0],
#             #                        lon = value[i][1])
#             if i > 0:
#                 graph.add_edge(prev_value, (lat,lon))
#
#             prev_value = (lat,lon)
#
#     return graph

def closest_node(node, nodes):
    node_list = []
    for elem in nodes:
        node_list.append((elem['x'],elem['y']))
    return nodes[cdist([node], node_list).argmin()]

def display_network(network):
    string_network = ""
    for route in network:
        elem = network.get(route)
        string_network = string_network + str(route) + ":"
        print(len(elem))
        for node in elem:
            string_network = string_network + str(node.coordinates) + " "
        string_network = string_network +"\n"

    print(string_network)




def reverse_geocode(source, dest):
    geolocator = Nominatim()
    location = geolocator.reverse(source)
    print((location.raw["osmid"]))

def get_shortest_path_line_string_local(graph,source,dest):
    dict_nodes = [d for n, d in graph.nodes_iter(data=True)]
    list_nodes = []
    for elem in dict_nodes:
        list_nodes.append(elem)

    closest_node_source = closest_node(source, list_nodes)
    closest_node_dest = closest_node(dest, list_nodes)

    if(nx.has_path(graph,closest_node_source['osmid'],closest_node_dest['osmid'])):
        return nx.shortest_path(graph, closest_node_source['osmid'], closest_node_dest['osmid'])
    else: return {}



def get_shortest_path_line_string(graph,source,dest):
    print("GET FROM POINT")
    print(source)
    print(dest)
    G_source = ox.graph_from_point((source[1],source[0]), distance=300, network_type='drive')
    G_dest = ox.graph_from_point((dest[1],dest[0]), distance=300, network_type='drive')

    dict_nodes = [d for n, d in G_source.nodes_iter(data=True)]
    list_nodes = []
    for elem in dict_nodes:
        list_nodes.append(elem)

    closest_node_source = closest_node(source, list_nodes)
    dict_nodes = [d for n, d in G_dest.nodes_iter(data=True)]
    list_nodes = []
    for elem in dict_nodes:
        list_nodes.append(elem)

    closest_node_dest = closest_node(dest, list_nodes)
    # nx.adjacency_matrix(graph,nodelist=)
    return nx.shortest_path(graph, closest_node_source['osmid'], closest_node_dest['osmid'])

def get_total_distance_intersections(map_graph,source_coordinates,dest_coordinates,osm_id_list):
    distance = 0
    map_graph_dict = [d for n, d in map_graph.nodes_iter(data=True)]
    temp_coordinate = (source_coordinates[0],source_coordinates[1])
    for i in range(0,len(osm_id_list)):
        for elem in map_graph_dict:
            if(osm_id_list[i] == elem["osmid"]):
                print(source_coordinates)
                print(str((elem["x"],elem["y"])))
                distance = distance + euclidean(temp_coordinate,(elem["x"],elem["y"]))
                print(distance)
                temp_coordinate = (elem["x"],elem["y"])

    distance = distance + euclidean(temp_coordinate,(dest_coordinates[0],dest_coordinates[1]))

    return distance




def convert_to_graph(self,coord_list):
    graph = nx.Graph()
    for j in range(0, len(coord_list)):
        graph.add_node(j, lat=coord_list[j][0], lon=coord_list[j][1])

    return graph

def get_nodes_shortest_path(shortest_path_nodes, graph):
    new_graph = nx.Graph()

    for k_y, v_y in graph.nodes_iter(data=True):
        for elem in shortest_path_nodes:
            if elem == k_y:
                new_graph.add_node(k_y, lat=v_y.get('lat'), lon=v_y.get('lon'), route_id = v_y.get('route_id'))

    print("GRAPHHH")
    print (graph.nodes(data=True))

    return graph

def convert_to_geo_latlong(coordinates):
    coordinates_list_temp = []

    for i in coordinates:
        coordinates_list_temp.append(geo.LatLon(i[0],i[1]))

    return coordinates_list_temp

def plot_line_graph(value_list):

    plt.plot(value_list, np.arange(len(value_list)))
    plt.ylabel('Fitness Score')
    plt.show()

















