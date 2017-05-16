# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import math
import numpy as np
import operator as op

from vtown.geo.polygon import Polygon
from .utils import convert_point_to_coordinate, convert_coordinates_to_nodes, get_location_bounds


class StopLayout(object):
    def __init__(self, max_num_nodes, max_walking_dist):
        self.max_num_nodes = max_num_nodes
        self.max_walking_dist = max_walking_dist


class LatticeLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist, lattice_start_coord):
        super(LatticeLayout, self).__init__(max_num_nodes, max_walking_dist)
        self.lattice_start_coord = lattice_start_coord

    def generate(self):
        dimension = int(math.ceil(math.sqrt(self.max_num_nodes)))
        coordinates = []

        for i in range(1, dimension + 1):
            for j in range(1, dimension + 1):
                lat = float(self.lattice_start_coord[0]) + float(float(self.max_walking_dist / 111111) * float(i))
                lng = float(self.lattice_start_coord[1] + float(float(self.max_walking_dist / 111111) * float(j)))
                coordinates.append((lat, lng))

        coordinates = coordinates[:int(len(coordinates) - (math.pow(dimension, 2) - self.max_num_nodes))]
        return convert_coordinates_to_nodes(coordinates)


class RandomLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist, location_geometry):
        super(RandomLayout, self).__init__(max_num_nodes, max_walking_dist)
        self.location_bounds = get_location_bounds(location_geometry)

    def generate(self):
        polygon = Polygon(*self.location_bounds)
        coordinates = [convert_point_to_coordinate(polygon.random_point()) for _ in range(self.max_num_nodes)]
        return convert_coordinates_to_nodes(coordinates)


class NBlobLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist, predefined_means, covariance_coefficient):
        super(NBlobLayout, self).__init__(max_num_nodes, max_walking_dist)
        self.predefined_means = predefined_means
        self.covariance_coefficient = covariance_coefficient

    def generate(self):
        diagonal_covariance = (self.covariance_coefficient / 1111111, -20 / 1111111)
        spherical_covariance = (-20 / 1111111, self.covariance_coefficient / 1111111)
        covariances = (diagonal_covariance, spherical_covariance)

        size = op.floordiv(self.max_num_nodes, len(self.predefined_means))

        coordinates = []
        for means in self.predefined_means:
            random_samples = np.random.multivariate_normal(means, covariances, size).T
            coordinates.extend(zip(random_samples[0], random_samples[1]))

        return convert_coordinates_to_nodes(coordinates)
