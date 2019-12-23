from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
from singleton import Singleton
import pyproj
import math
import numpy as np


class Satellite:
    def __init__(self, id, line1, line2, size=10):
        self.satellite = twoline2rv(line1, line2, wgs84)
        self.id = id
        self.size = size
        self.scale = 10
        self.ecef = Singleton.get_instance().get_data('ecef')
        self.lla = Singleton.get_instance().get_data('lla')
        self.a = self._get_semi_major_axis(line2[52:63])

    @staticmethod
    def get_static_position(sat, time):
        position = sat.get_propagation(time)
        longitude, latitude, radius = pyproj.transform(sat.ecef, sat.lla, position[0], position[1], position[2], radians=False)
        if math.isnan(longitude) or math.isnan(latitude) or math.isnan(radius):
            return None
        return {'latitude': latitude, 'longitude': longitude, 'height': radius, 'size': sat.size, 'id': sat.id}

    def get_propagation(self, time):
        position, velocity = self.satellite.propagate(time.year, time.month, time.day, time.hour, time.minute,
                                                      time.second)
        x, y, z = position
        return np.array([x * 1000, y * 1000, z * 1000])

    def get_position(self, time):
        position = self.get_propagation(time)
        longitude, latitude, radius = pyproj.transform(self.ecef, self.lla, position[0], position[1], position[2], radians=False)
        if math.isnan(longitude) or math.isnan(latitude) or math.isnan(radius):
            return None
        return {'latitude': latitude, 'longitude': longitude, 'height': radius, 'size': self.size, 'id': self.id}

    def _get_semi_major_axis(self, n):
        return (math.pow(3.986004418e14, 1/3)) / (math.pow((2 * float(n) * math.pi / 86400), 2/3))

    def get_semi_major_axis(self):
        return self.a

    def set_size(self, size):
        self.size = size