from timekeeper import TimeKeeper
from station import Station
import numpy as np

time_keeper = TimeKeeper()

class Tree:
    def __init__(self, root_data):
        self.root = Node(None, root_data)

    def get_shortest_path(self):
        shortest = []
        endnodes = []
        dist = 0
        self.traverse(self.root, endnodes)
        if len(endnodes) > 0:
            node = sorted(endnodes, key=lambda x: x.distance)[0]
            dist = node.distance
            while node.parent:
                shortest.append({'id': '{}|{}'.format(node.data.id, node.parent.data.id)})
                node = node.parent
        return shortest, dist

    def traverse(self, node, endnodes):
        if isinstance(node.data, Station) and not node.left and not node.right:
            endnodes.append(node)
        else:
            if node.left:
                self.traverse(node.left, endnodes)
            if node.right:
                self.traverse(node.right, endnodes)

class Node:
    def __init__(self, parent, data):
        self.parent = parent
        self.data = data
        self.distance = 0 if not parent else self.distance(parent, data)
        self.left = None
        self.right = None

    def insert(self, left, right):
        self.left = Node(self, left)
        self.right = Node(self, right)
        return self.left, self.right

    def traverse(self, node):
        if node is None:
            return
        else:
            print(node.data)
            self.traverse(node.left)
            self.traverse(node.right)

    @staticmethod
    def distance(parent, node_data):
        a = parent.data.get_ecef_position() if isinstance(parent.data, Station) else parent.data.get_propagation(time_keeper.get_time())
        b = node_data.get_ecef_position() if isinstance(node_data, Station) else node_data.get_propagation(time_keeper.get_time())
        return np.linalg.norm(a - b) + parent.distance
