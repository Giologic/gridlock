from __future__ import absolute_import, division

import networkx as nx
import numpy as np
import random
import routegenerator as ru
import sys
from tqdm import tqdm


from preprocessor.utils import get_location_road_graph
from routegenerator.computations import generate_route_network
from routegenerator.utils import add_distance_to_graph, merge_list_graphs, convert_to_list_graph, snap_route_network_to_road



def perform_genetic_algorithm(stop_nodes, list_graphs,
                              max_walking_dist, num_evolutions, num_generated_network_mutations_per_evolution,
                              route_mutation_probabilities,
                              fraction_of_nodes_to_remove, weight_random_failure, weight_targeted_failure, weight_gyration):
    location_road_graph = get_location_road_graph()

    for ig in list_graphs:
        print ("List Grahps")
        print(ig.edges(data=True))
        print(ig.nodes(data=True))

    for i in range(num_evolutions):
        num_mutations = np.random.choice(len(route_mutation_probabilities), 1, route_mutation_probabilities)[0]

        mutations = []
        if num_mutations > 0:
            print ("Begin Evolution: " + str(i))
            print("Number of mutable routes" + str(num_mutations))
            for j in range(num_generated_network_mutations_per_evolution):
                print("Begin Mutation" + str(j))
                # if num_mutations > 0 then randomly select n (which is ALSO EQUAL to num_mutations)
                #  routes to be replaced by a new route
                # replace the routes with the newly generated routes
                # append the modified network to the mutations list
                mutation_route_network = list_graphs
                print("Generating New Network with " + str(num_mutations) + " routes")
                new_route_network = generate_route_network(stop_nodes, max_walking_dist, num_mutations)
                print("Snapping Network To Road")
                new_snapped_route_network = snap_route_network_to_road(new_route_network)[2]
                print("Replacement of Routes Initiated...")
                for k in range(0, num_mutations):
                    selected_route_index = np.random.randint(len(list_graphs))
                    print ("Selected Route Index" + str(selected_route_index))
                    print ("Replacing ...")
                    print (mutation_route_network[selected_route_index].edges(data=True))
                    mutation_route_network[selected_route_index] = new_snapped_route_network[k]
                    print ("Replaced With... ")
                    print(new_route_network[k].edges(data=True))

                    print ("Setting new Edge Attr" + str(selected_route_index) + "as route_id")
                    nx.set_edge_attributes(mutation_route_network[selected_route_index], 'route_id', selected_route_index)
                    print (mutation_route_network[selected_route_index].edges(data=True))
                    print ("SET -> Merge")
                    merged_graph = merge_list_graphs(mutation_route_network)
                    print ("Merged")
                mutations.append(merged_graph)
                print ("Appending ")

        # pick the highest scoring mutation among the num_generated_network_mutations_per_evolution
        # mutations.append(ru.snap_route_network_to_road(road_snapped_network, output_graph=True))
        for mut in mutations:
            print("MUTATIONS")
            mut.nodes(data=True)
            mut.edges(data=True)

        if(mutations > 0):
            list_graphs = select_highest_scoring_mutation(mutations, fraction_of_nodes_to_remove, weight_random_failure, weight_targeted_failure ,weight_gyration)

    print("DONE")
    # return snap_route_network_to_road(list_graphs)


def select_random_routes(route_network, num_routes):
    return random.sample(route_network, num_routes)


def select_highest_scoring_mutation(candidate_road_snapped_networks, fraction_of_nodes_to_remove, weight_random_failure, weight_targeted_failure , weight_radius_of_gyration):
    max_fitness_score = -np.inf
    max_candidate_route_snapped_network = None

    for n in candidate_road_snapped_networks:
        fitness_score = compute_fitness_score(n, fraction_of_nodes_to_remove,
                                              weight_random_failure, weight_targeted_failure, weight_radius_of_gyration)
        if fitness_score > max_fitness_score:
            max_fitness_score = fitness_score
            max_candidate_route_snapped_network = n

    print ("MAXIMUM FITNESS SCORE: " + str(max_fitness_score))
    return convert_to_list_graph(max_candidate_route_snapped_network)

def generate_analytics_failure(graph,fraction_of_nodes_to_remove):
    route_network_list = []
    route_network = graph
    print (route_network.nodes())
    NetworkSize = len(route_network.nodes()) #network size to use in experiments
    num_removals = int(fraction_of_nodes_to_remove * NetworkSize) #number of nodes to remove
    route_network_list.append(route_network)
#     orig_route_network = copy.deepcopy(route_network_list)
    net_stat = all_network_statistics(route_network_list)
    route_ave_diameters, route_ave_path_lengths, route_ave_S = experiments(route_network_list, num_removals, run_fail = True)

    route_ave_diameters = route_ave_diameters[0]
    route_ave_path_lengths = route_ave_path_lengths[0]
    route_ave_S = route_ave_S[0]
    print (str(route_ave_path_lengths) + "/" + str(route_ave_diameters))
    return route_ave_path_lengths/route_ave_diameters

def generate_analytics_attack(graph,fraction_of_nodes_to_remove):

    route_network_list = []
    route_network = graph
    NetworkSize = len(route_network.nodes()) #network size to use in experiments
    num_removals = int(fraction_of_nodes_to_remove * NetworkSize) #number of nodes to remove

#     nx.draw(route_network)
#     plt.show()
    route_network_list.append(route_network)
#     orig_route_network = copy.deepcopy(route_network_list)
#     net_stat = all_network_statistics(route_network_list)

    route_ave_diameters, route_ave_path_lengths, route_ave_S = experiments(route_network_list, num_removals, run_fail = False)

    route_ave_diameters = route_ave_diameters[0]
    route_ave_path_lengths = route_ave_path_lengths[0]
    route_ave_S = route_ave_S[0]
    print (str(route_ave_path_lengths) + "/" + str(route_ave_diameters))
    return route_ave_path_lengths/route_ave_diameters

def compute_fitness_score(road_snapped_network_graph, fraction_of_nodes_to_remove,
                          weight_random_failure, weight_targeted_failure, weight_radius_of_gyration):
    G = road_snapped_network_graph.copy()
    G2 = road_snapped_network_graph.copy()
    G3 = road_snapped_network_graph.copy()
    random_failure_robustness = generate_analytics_failure(G, fraction_of_nodes_to_remove)
    print ("Weight" + str(weight_random_failure))
    print ("Failure Robustness " + str(random_failure_robustness))
    weighted_random_failure_robustness = weight_random_failure * random_failure_robustness

    targeted_failure_robustness = generate_analytics_attack(G2, fraction_of_nodes_to_remove)
    print ("Weight" + str(weight_targeted_failure))
    print ("Targeted Robustness " + str(targeted_failure_robustness))
    weighted_targeted_failure_robustness = weight_targeted_failure * targeted_failure_robustness

    radius_of_gyration = compute_radius_of_gyration(add_distance_to_graph(G3), len(G3.edges()), weight_radius_of_gyration)
    print ("Weight" + str(weight_radius_of_gyration))
    print ("Radius of Gyration " + str(radius_of_gyration))
    weighted_radius_of_gyration = weight_radius_of_gyration * radius_of_gyration


    print (weighted_radius_of_gyration)
    print (weighted_random_failure_robustness)
    print (weighted_targeted_failure_robustness)
    numerator = weighted_radius_of_gyration - weighted_random_failure_robustness - weighted_targeted_failure_robustness
    denominator = weight_random_failure + weight_targeted_failure + weight_radius_of_gyration
    fitness_score = numerator/denominator
    return fitness_score


def fail(G): #a python function that will remove a random node from the graph G
    n = random.choice(G.nodes())  #pick a random node
    G.remove_node(n) # remove that random node, attached edges automatically removed.

def attack_degree(G): #remove node with maximum degree
    degrees = G.degree() # get dcitonary where key is node id, value is degree
    max_degree = max(degrees.values()) # find maximum degree value from all nodes
    max_keys = [k for k,v in degrees.items() if v==max_degree] #get all nodes who have the maximum degree (may be more than one)
    G.remove_node(max_keys[0]) #remove just the first node with max degree, we will remove others next

def attack_betweenness(G): #note - not currently used, but try it!
    betweenness = nx.betweenness_centrality(G) # get dictionary where key is node id and value is betweenness centrality
    max_betweenenss = max(betweenness.values()) # find maximum degree value from all nodes
    max_keys = [k for k,v in betweenness.items() if v==max_betweenness] #get all nodes who have the maximum degree (may be more than one)
    G.remove_node(max_keys[0]) #remove just the first node with max degree, we will remove others next


def diameter_ave_path_length(G):
    # We create our own function to do this so things are slightly faster,
    # we can calculate diameter and avg path length at the same time
    max_path_length = 0
    total = 0.0
    for n in G: #iterate over all nodes
     path_length=nx.single_source_shortest_path_length(G, n) # generate shortest paths from node n to all others
     total += sum(path_length.values()) #total of all shortest paths from n
     if max(path_length.values()) > max_path_length: #keep track of longest shortest path we see.
         max_path_length = max(path_length.values())
    try:
     avg_path_length = total / (G.order()*(G.order() - 1))
    except ZeroDivisionError:
     avg_path_length = 0.0
    return max_path_length, avg_path_length

def all_network_statistics(nw_list):
# a function that takes in a list of networks and returns 3 lists of same length listing the diameter, average
# path length and giant component size for all the networks
    diameters = []
    path_lengths = []
    S = []
    for n in nw_list:
      d,l,s = a_network_statistics(n)
      diameters.append(d)
      path_lengths.append(l)
      S.append(s)
    return diameters, path_lengths, S

def a_network_statistics(n):
     Gcc=sorted(nx.connected_component_subgraphs(n), key = len, reverse=True)
     G0=Gcc[0]
     d,l = diameter_ave_path_length(G0)
     s = float(G0.order()) / float(len(n.nodes()))
     return d,l,s

def experiments(networks, removals, run_fail=True, measure_every_X_removals=20):
     # the below list will record the average statistic for all networks, a new entry in the list is added after each fail
     ave_diameters = []
     ave_path_lengths = []
     ave_S = []
     sys.stderr.write("---- Starting Experiments ---- \n")
     sys.stderr.flush()
     for x in tqdm(range(removals)):
         for n in networks:
             if run_fail:
                 fail(n)
             else:
                 attack_degree(n)
         if x % measure_every_X_removals == 0:
             d, l, s = all_network_statistics(networks)
             ave_diameters.append(np.mean(d))
             ave_path_lengths.append(np.mean(l))
             ave_S.append(np.mean(s))
     sys.stderr.write("---- Experiments Finished ---- \n")
     sys.stderr.flush()
     return ave_diameters, ave_path_lengths, ave_S

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
                Y[(str(k_x), str(k_y))] = float(dp[(str(k_x), str(k_y))])/float(dw)
            else:
                Y[(str(k_x), str(k_y))] = 0.0

    return Y


def _get_distance_individual(graph):
    T = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                accumulated_distance = 0.0
                if(len(shortest_path_nodes) > 1):
                    for i in range(0, len(shortest_path_nodes) - 1):
                        edge = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('distance')
                        accumulated_distance = float(accumulated_distance) + float(edge)
                    T[(str(k_x),str(k_y))] = accumulated_distance
                else:
                    T[(str(k_x), str(k_y))] = 0
            else:
                T[(str(k_x), str(k_y))] = 0

    return T


# new gettwd does not use weighted adjacency matrix
def _get_total_weighted_distance(graph, weight):
    # A = _create_weighted_adjacency_matrix(graph)
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


def _create_weighted_adjacency_matrix(graph):
    w = 10
    adjacency_matrix = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                accumulated_distance = 0.0

                if len(shortest_path_nodes) > 1:
                    for i in range(0, len(shortest_path_nodes) - 1):
                        edge = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('dist')
                        accumulated_distance = float(accumulated_distance) + float(edge)

                    adjacency_matrix[(str(k_x), str(k_y))] = accumulated_distance
                else:
                    adjacency_matrix[(str(k_x), str(k_y))] = 0
            elif not nx.has_path(graph, k_x, k_y):
                coordinate1 = (v_x["lat"], v_x["lon"])
                coordinate2 = (v_y["lat"], v_y["lon"])
                adjacency_matrix[(str(k_x), str(k_y))] = euclidean(coordinate1, coordinate2) * w
            elif k_x == k_y:
                adjacency_matrix[(str(k_x), str(k_y))] = 0

    return adjacency_matrix


def euclidean(x, y):
    sum_square = 0.0
    for i in range(len(x)):
        sum_square += (x[i] - y[i]) ** 2

    return sum_square ** 0.5


def get_nodes_shortest_path(shortest_path_nodes, graph):
    new_graph = nx.Graph()

    for k_y, v_y in graph.nodes_iter(data=True):
        for elem in shortest_path_nodes:
            if elem == k_y:
                new_graph.add_node(k_y, lat=v_y.get('lat'), lon=v_y.get('lon'), route_id = v_y.get('route_id'))

    return graph


def _get_no_of_transfers(graph):
    temp = []
    p = graph.copy()
    no_of_tranfer = 0

    for k_y, v_y in p.nodes_iter(data=True):
        if (len(p.nodes()) > 1):
            if str(v_y.get("route_id")) not in temp:
                temp.append(str(v_y.get("route_id")))
            no_of_transfer = len(temp)-1
        else:
            no_of_tranfer = 0

    return no_of_tranfer