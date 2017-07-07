import random
import numpy
import networkx as nx
from . import old_robustness as rb

from routegenerator.old_computations import create_road_snapped_network, generate_route
from routegenerator.old_utils import euclidean, get_nodes_shortest_path

def _generate_chosen_route_list(network, num_routes):
    selected_route_list_index = []
    # print(range(len(network)))
    selected_routes = random.sample(range(len(network)), num_routes)
    for element in selected_routes:
        network.get(element)
        selected_route_list_index.append(element)

    return selected_route_list_index

def __robustness_failure(graph, num_removals):
    networks = []
    networks.append(graph)
    ave_diameters, ave_path_lengths, ave_S= rb.experiments(networks, num_removals)
    return  ave_diameters, ave_path_lengths, ave_S

def __robustness_attack(graph, num_removals):
    networks = []
    networks.append(graph)
    ave_diameters, ave_path_lengths, ave_S = rb.experiments(networks, num_removals, run_fail= False)
    return ave_diameters, ave_path_lengths, ave_S

#rand_sample_value - for random sampling in the summing up of efficiency of source and destination pairs
def __radius_of_gyration(graph, no_rand_sample_value):
    print("IN RADIUS OF GYRATION: ")
    print(graph.edges(data=True))

    #w,h = graph.length, graph.length;
    #A = [[0 for x in range(w)] for y in range(h)]

    #serves as weighted Matrix A

    #10 = arbitrary penalty weight for walking based from Pang et al's paper
    A = _create_weighted_adjacency_matrix(graph)



    #_______________________________________________________
    #serves as number of Transfers
    # T = {}
    #
    # total_distance = {}
    # nodes_x = [d for n, d in graph.nodes_iter(data=True)]
    # nodes_y = [d for n, d in graph.nodes_iter(data=True)]
    #
    # for k_x, v_x in graph.nodes_iter(data=True):
    #     for k_y, v_y in graph.nodes_iter(data=True):
    #         if nx.has_path(graph, k_x, k_y):        #not sure if this line should be removed
    #             shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
    #             accumulated_distance = 0.0
    #             if (len(shortest_path_nodes) > 1):
    #                 for i in range(0, len(shortest_path_nodes) - 1):
    #                     edge = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('dist')
    #                     print(edge)
    #                     accumulated_distance = float(accumulated_distance) + float(edge)
    #                  total_distance[str(k_x)][str(k_y)] = accumulated_distance

    #get number of transfers per source-destination pair
    # for k_x, v_x in total_distance.items():
    #     temp = []
    #     for k_y in range(0,len(total_distance)):
    #         if total_distance[str(k_x)][str(k_y)]["route_id"] not in temp:
    #             temp.append(total_distance[str(k_x)][str(k_y)]["route_id"])
    #         T[str(k_x)][str(k_y)] = len(temp)-1
    #
    # total_weighted_distance = {}
    w2 = 20

    # for k_x in total_distance:
    #     for k_y in range(0, len(k_x)):
    #         total_weighted_distance[str(k_x)][str(k_y)] = A[str(k_x)][str(k_y)] * total_distance[str(k_x)][str(k_y)] + w2 * T[str(k_x)][str(k_y)]


    # ..........................editing this part
    # total_weighted_distance =

    # for x in total_dist:
    #    for y in total_dist :
    #     total_weighted_distance[x][y] = A[x][y]*total_dist[x][y] + w2*T[x][y]

    # y_weighted_distance = {}
    #
    # for k_x in total_weighted_distance:
    #     for k_y in range(0, len(k_x)):
    #         y_weighted_distance[str(k_x)][str(k_y)] = total_distance[str(k_x)][str(k_y)]/total_weighted_distance[str(k_x)][str(k_y)]
    #
    # # for key, value in sorted(y_weighted_distance.items(), key=lambda x: random.random()):
    # efficiency_sum_per_pair = y_weighted_distance
    # #rand_sample_val = 1000
    # random.shuffle(efficiency_sum_per_pair)
    # #for key, value in efficiency_sum_per_pair:
    # efficiency_sum_list = random.sample(efficiency_sum_per_pair, no_rand_sample_value)
    # efficiency_sum = 0.0
    # for k_x in efficiency_sum_list:
    #     for k_y in range(0, len(k_x)):
    #         efficiency_sum = efficiency_sum + efficiency_sum_list[str(k_x)][str(k_y)]

    w = 20 # weight for transfer
    no_of_random_values = 100 # number of y weighted efficiency per path to consider to be randomly summed up

    return _get_efficiency_sum(graph, no_rand_sample_value, w2)

def _create_weighted_adjacency_matrix(graph):
    print("WEIGHTED ADJACENCY MATRIX")
    print(graph.edges(data=True))

    w = 10
    A = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                accumulated_distance = 0.0
                print("SHORTEST PATH :")
                print(len(shortest_path_nodes))
                print(shortest_path_nodes)
                if(len(shortest_path_nodes) > 1):
                    for i in range(0, len(shortest_path_nodes) - 1):
                        edge = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('dist')
                        print(edge)
                        accumulated_distance = float(accumulated_distance) + float(edge)

                    A[(str(k_x),str(k_y))] = accumulated_distance
                    # PAUSED HERE CHECK PAPER FOR WEIGHTED DISTANCE MATRIX
                else:
                    A[(str(k_x),str(k_y))] = 0
            elif not nx.has_path(graph, k_x, k_y):
                # Create an accurate fix
                # shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                # accumulated_distance = 0.0
                # for i in range(0, len(shortest_path_nodes) - 1):
                #     accumulated_distance = accumulated_distance + (
                #     graph.edges(shortest_path_nodes[i], shortest_path_nodes[i + 1]))

                coordinate1 = (v_x["lat"], v_x["lon"])
                coordinate2 = (v_y["lat"], v_y["lon"])
                A[(str(k_x),str(k_y))] = euclidean(coordinate1, coordinate2) * w
            elif k_x == k_y:
                A[(str(k_x), str(k_y))] = 0

    print(A)

    return A

def _get_distance_individual(graph):
    print ("IN GET Dp: ")
    print(graph.edges(data=True))

    T = {}

    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                accumulated_distance = 0.0
                print("SHORTEST PATH :")
                print(len(shortest_path_nodes))
                print(shortest_path_nodes)
                if(len(shortest_path_nodes) > 1):
                    for i in range(0, len(shortest_path_nodes) - 1):
                        edge = graph.get_edge_data(shortest_path_nodes[i], shortest_path_nodes[i + 1]).get('dist')
                        print(edge)
                        accumulated_distance = float(accumulated_distance) + float(edge)
                    T[(str(k_x),str(k_y))] = accumulated_distance
                else:
                    T[(str(k_x), str(k_y))] = 0
            else:
                T[(str(k_x), str(k_y))] = 0
    print(T)

    return T

def _get_total_distance(graph):
    print("IN GET TOTAL DISTANCE: ")

    T = _get_distance_individual(graph)
    accumulated_total_distance = 0.0
    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            accumulated_total_distance = float(accumulated_total_distance) + float(T[(str(k_x),str(k_y))])

    return accumulated_total_distance


#returns number of transfer given a source-destination pair
def _get_no_of_transfers(graph):
    temp = []
    p = graph.copy()
    no_of_tranfer = 0
    print ("PATH")
    print(p.nodes(data=True))

    for k_y, v_y in p.nodes_iter(data=True):
        if (len(p.nodes()) > 1):
            if str(v_y.get("route_id")) not in temp:
                temp.append(str(v_y.get("route_id")))
            no_of_transfer = len(temp)-1
        else:
            no_of_tranfer = 0

    return no_of_tranfer

#weight is usually 20
def _get_total_weighted_distance(graph, weight):
    print("IN GET TOTAL WEIGHTED DISTANCE")

    A = _create_weighted_adjacency_matrix(graph)
    dp = _get_distance_individual(graph)
    w = weight
    total_weighted_distance = 0.0 #accumulated total weighted distance
    T = {}
    for k_x, v_x in graph.nodes_iter(data=True):
        for k_y, v_y in graph.nodes_iter(data=True):
            if nx.has_path(graph, k_x, k_y):
                shortest_path_nodes = nx.shortest_path(graph, k_x, k_y)
                g = get_nodes_shortest_path(shortest_path_nodes, graph)
                T = _get_no_of_transfers(g)
            a = float(A[(str(k_x), str(k_y))])
            b = float(dp[(str(k_x), str(k_y))])
            weighted_distance =  a * b + (w * T)
            total_weighted_distance = float(total_weighted_distance) + float(weighted_distance)

    return total_weighted_distance

# return list of yweighted efficiency per path
def _get_yweighted_list(graph, weight):
    print("IN GET Y WEIGHT INDIVIDUAL: ")

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

# return sum of y weighted efficiency per path
def _get_efficiency_sum(graph, no_of_random_values, weight):
    print("IN GET EFFICIENCY SUM (Y_WEIGHT): ")

    efficiency_sum = 0.0
    weighted_list = _get_yweighted_list(graph, weight)
    efficiency_sum_list = random.sample(weighted_list.keys(), no_of_random_values)

    print ("EFFICIENCY")
    for k_x, k_y in efficiency_sum_list:
         temp = weighted_list[(str(k_x), str(k_y))]
         efficiency_sum = float(temp) + float(efficiency_sum)
    print("EFFICIENCY SUM MO TO!")
    print(efficiency_sum)
    return efficiency_sum



def _solve_for_fitness(graph,num_removals,no_rand_sample_value):
    print("IN FITNESS: " )
    print(graph.edges(data=True))
    w_attack = 0.2
    w_fail = 0.2
    w_radius = 0.6

    f_graph = graph.copy()
    a_graph = graph.copy()
    ave_diameters_f, ave_path_lengths_f, ave_S_f = __robustness_failure(f_graph, num_removals)
    ave_diameters_a, ave_path_lengths_a, ave_S_a = __robustness_attack(a_graph, num_removals)



    print(ave_diameters_f[0])
    print(ave_diameters_a[0])
    rob_fail = float(ave_diameters_f[0])/float(len(graph.nodes()) - 1)
    rob_attack = float(ave_diameters_a[0])/float(len(graph.nodes()) - 1)
    radius_of_gyration = float(__radius_of_gyration(graph,no_rand_sample_value))
    rob_fail_with_weight = float(w_fail) * float(rob_fail)
    rob_attack_with_weight =float(w_attack) * float(rob_attack)
    radius_of_gyration_with_weight = float(w_radius) * float(radius_of_gyration)
    print("ROBUSTNESS FAIL SCORE =  " + str(rob_fail))
    print("ROBUSTNESS ATTACK SCORE =  " + str(rob_attack))
    print("RADIUS OF GYRATION SCORE =  " + str(radius_of_gyration))
    print("WEIGHTED ROBUSTNESS FAIL SCORE =  " + str(rob_fail_with_weight))
    print("WEIGHTED ROBUSTNESS ATTACK SCORE = " + str(rob_attack_with_weight))
    print("WEIGHTED RADIUS OF GYRATION SCORE = " + str(radius_of_gyration_with_weight))

    score = radius_of_gyration_with_weight - rob_fail_with_weight - rob_attack_with_weight
    print("TOTAL SCORE: " + str(score))
    return rob_fail, rob_attack, radius_of_gyration ,rob_fail_with_weight, rob_attack_with_weight, radius_of_gyration_with_weight, score

def perform_genetic_algorithm(map_graph, stop_network, route_network, max_allow_walk_dist, num_routes, num_evolutions, num_mutations, num_removals, no_rand_sample_value, probabilities_list):
    ctr_evol = 0
    mutation_score_list = []
    current_evolution_route = None
    highest_scoring_mutation = None
    fitness_score_list = []
    while (ctr_evol <= num_evolutions):
        # print("PASS")
        selected_route_list_index = _generate_chosen_route_list(route_network, num_routes)
        # print("SELECTED_ROUTE_INDEX: " + str(selected_route_list_index))

        no_mutations_list = numpy.random.choice(num_routes, num_mutations, probabilities_list)
        ctr_mut = 0
        # print(no_mutations_list)
        candidate_mutations = []
        print(no_mutations_list)

        for mutation in no_mutations_list:
            # print(mutation)
            if(mutation > 0):
                for j in range(0, mutation):
                    new_route = generate_route(stop_network, max_allow_walk_dist, route_id=selected_route_list_index[j])
                    route_network[selected_route_list_index[j]] = new_route

                road_snapped_network_graph = create_road_snapped_network(map_graph, route_network)
                print("IN GENETIC: ")
                print(road_snapped_network_graph.edges(data=True))
                print(road_snapped_network_graph.nodes(data=True))
                rob_fail, rob_attack, radius_of_gyration, w_rob_fail, w_rob_attack, w_radius_of_gyration, fitness_score = _solve_for_fitness(graph=road_snapped_network_graph, num_removals=num_removals,
                                                   no_rand_sample_value=no_rand_sample_value)
                print(fitness_score)
                mutation_score_list.append([road_snapped_network_graph, rob_fail, rob_attack, radius_of_gyration, w_rob_fail, w_rob_attack, w_radius_of_gyration, fitness_score])
        ctr_evol = ctr_evol + 1

        print("MUTATION SCORE LIST: ")
        print(mutation_score_list)
        print("LEN : " + str(len(mutation_score_list)))

        if(len(mutation_score_list) == 0):
            return None
        else:
            highest_scoring_mutation = get_index_of_highest_mutation_score(mutation_score_list)
            print("HIGHEST SCORING MUTATION: ")
            print(highest_scoring_mutation)
            if(current_evolution_route == None):
                current_evolution_route = highest_scoring_mutation
            else:
                if(current_evolution_route[7] < highest_scoring_mutation[7]):
                    current_evolution_route = highest_scoring_mutation
                    print("MAX SCORE: " + str(highest_scoring_mutation[7]))

    return highest_scoring_mutation, fitness_score_list






def get_index_of_highest_mutation_score(mutation_score_list):

    max_score_index = None
    print("Mutation Score List Size: " + str(len(mutation_score_list)))
    for i in range(0,len(mutation_score_list)):
        if max_score_index is None:
            max_score_index = 0
        if(mutation_score_list[max_score_index][7] < mutation_score_list[i][7]):
            max_score_index = i



    if max_score_index is not None:
        max_network = mutation_score_list[max_score_index]
        return max_network
    else:
        return (0,None)


