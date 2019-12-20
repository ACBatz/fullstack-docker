import numpy as np
from station import Station

class RouteTree:
    def __init__(self, time, data, distance_function):
        self.time = time
        self.root = Node(data, 0)
        self.distance_function = distance_function

    def insert(self, node_data, min_angle, min_distance):
        self.found_node = None
        self.get_node(node_data)
        if not self.found_node:
            raise Exception
        else:
            node = self.found_node
        node.min_angle = Node(min_angle, self.get_distance(node_data, min_angle) + node.distance)
        node.min_distance = Node(min_distance, self.get_distance(node_data, min_angle) + node.distance)

    def get_node(self, data):
        self._get_node_recursive(data, self.root)

    def _get_node_recursive(self, data, currentNode):
        if currentNode.data == data:
            self.found_node = currentNode
        else:
            if currentNode.min_angle:
                self._get_node_recursive(data, currentNode.min_angle)
            if currentNode.min_distance:
                self._get_node_recursive(data, currentNode.min_distance)


    def get_distance(self, data0, data1):
        if isinstance(data0, Station):
            x0, y0, z0 = data0.get_ecef_position()
        else:
            x0, y0, z0 = data0.get_propagation(self.time)[0]
            x0 = 1000 * x0
            y0 = 1000 * y0
            z0 = 1000 * z0

        if isinstance(data1, Station):
            x1, y1, z1 = data1.get_ecef_position()
        else:
            x1, y1, z1 = data1.get_propagation(self.time)[0]
            x1 = 1000 * x1
            y1 = 1000 * y1
            z1 = 1000 * z1

        return self.distance_function(np.array([x0, y0, z0]), np.array([x1, y1, z1]))


class Node:
    def __init__(self, data, distance):
        self.data = data
        self.min_angle = None
        self.min_distance = None
        self.distance = distance
