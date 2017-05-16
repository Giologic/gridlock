# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def convert_point_to_coordinate(point):
    return point.x, point.y


def convert_coordinates_to_nodes(coordinates):
    return [Node(i, coordinates[i]) for i in range(0, len(coordinates))]


def get_location_bounds(location_geometry):
    return location_geometry['geometries'][0]['coordinates'][0][0]


class Node(object):
    def __init__(self, node_id, coordinates):
        self.node_id = node_id
        self.coordinates = coordinates
