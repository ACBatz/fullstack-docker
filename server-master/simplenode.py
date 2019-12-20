class SNode:
    def __init__(self, data):
        self.data = data
        self.parent = None
        self.angle = None
        self.distance = None

    def insert_pair(self, angle, distance):
        self.angle = angle
        self.distance = distance
        self.parent = self