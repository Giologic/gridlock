import networkx as nx #import NetworkX
import numpy as np #import numpy for ...
#force drawing of graphs inline for ipython notebook
# %matplotlib inline
import matplotlib.pyplot as plt #import matplotlib for plotting/drawing grpahs
import matplotlib.patches as mpatches #for legends in the graph
# from __future__ import unicode_literals #allow UTF characters in graph labels
import random # for random choice function
import copy # this is use for making deep copies of lists
from tqdm import tqdm #nice library for progress bars
import sys #for writing output to stderr

def fail(G):  # a python function that will remove a random node from the graph G
    n = random.choice(G.nodes())  # pick a random node
    G.remove_node(n)  # remove that random node, attached edges automatically removed.


def attack_degree(G):  # remove node with maximum degree
    degrees = G.degree()  # get dcitonary where key is node id, value is degree
    max_degree = max(degrees.values())  # find maximum degree value from all nodes
    max_keys = [k for k, v in degrees.items() if
                v == max_degree]  # get all nodes who have the maximum degree (may be more than one)
    G.remove_node(max_keys[0])  # remove just the first node with max degree, we will remove others next


def attack_betweenness(G):  # note - not currently used, but try it!
    betweenness = nx.betweenness_centrality(
        G)  # get dictionary where key is node id and value is betweenness centrality
    max_betweenness = max(betweenness.values())  # find maximum degree value from all nodes
    max_keys = [k for k, v in betweenness.items() if v == max_betweenness]  # get all nodes who have the maximum degree (may be more than one)
    G.remove_node(max_keys[0])  # remove just the first node with max degree, we will remove others next


def diameter_ave_path_length(G):
    # We create our own function to do this so things are slightly faster,
    # we can calculate diameter and avg path length at the same time
    max_path_length = 0
    total = 0.0
    for n in G:  # iterate over all nodes
        path_length = nx.single_source_shortest_path_length(G, n)  # generate shortest paths from node n to all others
        total += sum(path_length.values())  # total of all shortest paths from n
        if max(path_length.values()) > max_path_length:  # keep track of longest shortest path we see.
            max_path_length = max(path_length.values())
    try:
        avg_path_length = total / (G.order() * (G.order() - 1))
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
        d, l, s = a_network_statistics(n)
        diameters.append(d)
        path_lengths.append(l)
        S.append(s)
    return (diameters, path_lengths, S)


def a_network_statistics(n):
    NetworkSize = len(n)
    Gcc = sorted(nx.connected_component_subgraphs(n), key=len, reverse=True)
    G0 = Gcc[0]
    d, l = diameter_ave_path_length(G0)
    s = float(G0.order()) / float(NetworkSize)
    return d, l, s

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