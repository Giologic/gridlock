# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import cPickle as pickle
import json
import os
import osmnx as ox
import settings

from gridlock.settings import DATA_FILES_ROOT


def get_location_geometry(location):
    location_file = open(os.path.join(DATA_FILES_ROOT, location.path))
    return json.load(location_file)


def get_location_road_graph():
    road_graph_cache_path = os.path.join(settings.DATA_FILES_ROOT,
                                         'gridlock/preprocessor/graphs/metromanila-graph-cache.pickle')
    if not os.path.exists(road_graph_cache_path):
        location_road_graph = ox.load_graphml(
            'gridlock/preprocessor/graphs/metromanila.gml', settings.DATA_FILES_ROOT)
        with open(road_graph_cache_path, 'w') as pickle_handle:
            pickle.dump(location_road_graph, pickle_handle)
        return location_road_graph

    else:
        with open(road_graph_cache_path) as pickle_handle:
            location_road_graph = pickle.load(pickle_handle)
            return location_road_graph
