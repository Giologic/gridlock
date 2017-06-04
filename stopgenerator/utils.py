# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def convert_point_to_latlng(point):
    return point.y, point.x


def convert_latlng_to_stop_nodes(latlng):
    return [StopNode(i, latlng[i]) for i in range(0, len(latlng))]


def get_location_bounds(location_geometry):
    return location_geometry['geometries'][0]['coordinates'][0][0]


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

