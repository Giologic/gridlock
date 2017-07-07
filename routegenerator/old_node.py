import itertools

class Node(object):

    _status = 0


    #MaxDegree

    def __init__(self, _node_id, coordinates):
        self._node_id = _node_id
        self._coordinates = coordinates
        self._route_id = 0
        self.enable()
        pass

    @property
    def node_id(self):
        return self._node_id

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def route_id(self):
        return self._route_id

    @node_id.setter
    def node_id(self, node_id):
        self._node_id = node_id

    @coordinates.setter
    def coordinates(self, coordinates):
        self._coordinates = coordinates

    @node_id.getter
    def node_id(self):
        return self._node_id

    @coordinates.getter
    def coordinates(self):
        return self._coordinates

    @route_id.setter
    def route_id(self, route_id):
        self._route_id = route_id

    @route_id.getter
    def route_id(self):
        return self._route_id

    def enable(self):
        self._status = 0

    def disable(self):
        self._status = 1

    def eliminate(self):
        self._status = 2

    def to_string_xy(self):
        return "(" + str(self.coordinates[0]) + "," + str (self.coordinates[1]) + ")"

def is_enabled():
    return 0

def is_disabled():
    return 1

def is_eliminated():
    return 2