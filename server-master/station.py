import pyproj
import numpy as np

class Station:
    def __init__(self, id, lat, long, alt, size=15):
        self.id = id
        self.lat = lat
        self.long = long
        self.alt = alt
        self.size = size
        self.ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        self.lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')

    def get_ecef_position(self):
        x, y, z = pyproj.transform(self.lla, self.ecef, self.long, self.lat, self.alt, radians=False)
        return np.array([x, y, z])

    def get_position(self):
        return {'latitude': self.lat, 'longitude': self.long, 'height': self.alt, 'size': self.size, 'id': self.id}
