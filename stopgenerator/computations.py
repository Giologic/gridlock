# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division

import math
import numpy as np
import operator as op

from vtown.geo.polygon import Polygon
from utils import convert_point_to_latlng, convert_latlng_to_stop_nodes, get_location_bounds


class StopLayout(object):
    def __init__(self, max_num_nodes, max_walking_dist):
        self.max_num_nodes = max_num_nodes
        self.max_walking_dist = max_walking_dist


class LatticeLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist, lattice_start_latlng):
        super(LatticeLayout, self).__init__(max_num_nodes, max_walking_dist)
        self.lattice_start_latlng = lattice_start_latlng

    def generate(self):
        dimension = int(math.ceil(math.sqrt(self.max_num_nodes)))
        latlng_list = []

        for i in range(1, dimension + 1):
            for j in range(1, dimension + 1):
                lat = float(self.lattice_start_latlng[0]) + float(float(self.max_walking_dist / 111111) * float(i))
                lng = float(self.lattice_start_latlng[1] + float(float(self.max_walking_dist / 111111) * float(j)))
                latlng_list.append((lat, lng))

        latlng_list = latlng_list[:int(len(latlng_list) - (math.pow(dimension, 2) - self.max_num_nodes))]
        return convert_latlng_to_stop_nodes(latlng_list)


class RandomLayout(StopLayout):
    def __init__(self, max_num_nodes, max_walking_dist, location_geometry):
        super(RandomLayout, self).__init__(max_num_nodes, max_walking_dist)
        self.location_bounds = get_location_bounds(location_geometry)

    def generate(self):
        polygon = Polygon(*self.location_bounds)
        latlng_list = [convert_point_to_latlng(polygon.random_point()) for _ in range(self.max_num_nodes)]
        return convert_latlng_to_stop_nodes(latlng_list)


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

        latlng_list = []
        for means in self.predefined_means:
            random_samples = np.random.multivariate_normal(means, covariances, size).T
            latlng_list.extend(zip(random_samples[1], random_samples[0]))

        return convert_latlng_to_stop_nodes(latlng_list)
