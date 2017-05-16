# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import math
from vtown.geo.polygon import Polygon


def convert_point_to_coordinate(point):
    return point.x, point.y


def convert_coordinates_to_nodes(coordinates):
    return [Node(i, coordinates[i]) for i in range(0, len(coordinates))]


class Node(object):
    def __init__(self, node_id, coordinates):
        self.node_id = node_id
        self.coordinates = coordinates

    def __str__(self):
        return "Node #" + str(self.node_id) + " - " + str(self.coordinates)


class StopLayout(object):
    def __init__(self, max_num_nodes, max_walking_dist, layout_coord):
        self.max_num_nodes = max_num_nodes
        self.max_walking_dist = max_walking_dist
        self.layout_coord = layout_coord


class LatticeLayout(StopLayout):
    def generate(self):
        dimension = int(math.ceil(math.sqrt(self.max_num_nodes)))
        coordinates = []

        for i in range(1, dimension + 1):
            for j in range(1, dimension + 1):
                lat = float(self.layout_coord[0]) + float(float(self.max_walking_dist / 111111) * float(i))
                lng = float(self.layout_coord[1] + float(float(self.max_walking_dist / 111111) * float(j)))
                coordinates.append((lat, lng))

        coordinates = coordinates[:int(len(coordinates) - (math.pow(dimension, 2) - self.max_num_nodes))]
        return convert_coordinates_to_nodes(coordinates)


class RandomLayout(StopLayout):
    def generate(self):
        polygon = Polygon(*self.layout_coord['geometries'][0]['coordinates'][0][0])
        coordinates = [convert_point_to_coordinate(polygon.random_point()) for _ in range(self.max_num_nodes)]
        return convert_coordinates_to_nodes(coordinates)


class NBlobLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist,
                 layout_coord, predefined_means, covariance_coefficient):
        super(NBlobLayout, self).__init__(max_num_nodes, float(max_walking_dist / 111111), layout_coord)
        self.predefined_means = predefined_means
        self.covariance_coefficient = covariance_coefficient

    def generate(self):
        pass
