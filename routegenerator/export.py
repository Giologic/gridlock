import networkx as nx

from routegenerator.utils import convert_uuid_route
from networkoptimizer.computations import euclidean


def prepare_graph_for_export(graph, location_road_nodes):
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
