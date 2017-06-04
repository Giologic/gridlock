# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np

from scipy.spatial.distance import cdist


def convert_point_to_latlng(point):
    return point.y, point.x


def convert_latlng_to_stop_nodes(latlng):
    return [StopNode(i, latlng[i]) for i in range(0, len(latlng))]


def get_location_bounds(location_geometry):
    return location_geometry['geometries'][0]['coordinates'][0][0]


def enable_stop_nodes(stop_nodes):
    for n in stop_nodes:
        n.enable()


def all_nodes_disabled(stop_nodes):
    return get_num_disabled(stop_nodes) == len(stop_nodes)


def get_num_disabled(stop_nodes):
    return sum(1 for n in stop_nodes if not n.enabled)


def closest_node(nodes, source_node):
    distances = cdist(np.asarray([source_node.latlng]), np.asarray([n.latlng for n in nodes]))
    return nodes[distances.argmin()]


class StopNode(object):
    def __init__(self, uuid, latlng):
        self.uuid = uuid
        self.latlng = latlng
        self.enabled = True
        self.route_id = None

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
