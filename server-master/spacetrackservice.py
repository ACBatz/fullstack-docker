import requests
import logging
import datetime

from satellite import Satellite

# logging.basicConfig(filename='satellite.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

class SatelliteTrackService:
    def __init__(self):
        # response = requests.get('http://www.celestrak.com/NORAD/elements/active.txt')
        pass

    @staticmethod
    def get_satellite_data():
        response = open('active.txt', 'r').readlines()
        splits = response
        satellites = []
        size = 5
        for i in range(0, len(splits) - 1, 3):
            satellite = Satellite(id=splits[i].replace(' ', '').replace('\n', ''), line1=splits[i+1].replace('\n', ''), line2=splits[i+2].replace('\n', ''), size=size)
            satellites.append(satellite)
        satellites.sort(key=lambda x: x.get_semi_major_axis())
        satellites = satellites[:1250 if len(satellites) >= 1250 else len(satellites)]
        print('Retrieved [{}] satellites from Celestrak'.format(len(satellites)))
        return satellites

    @staticmethod
    def get_more_satellite_data():
        response = open('TLE.txt', 'r').readlines()
        splits = response
        satellites = []
        size = 5
        for i in range(0, len(splits) - 1, 2):
            print(i)
            satellite = Satellite(id=splits[i].replace('  ', '').split(' ')[2],
                                  line1=splits[i].replace('\n', ''), line2=splits[i + 1].replace('\n', ''),
                                  size=size)
            satellites.append(satellite)
        print('Retrieved [{}] satellites from Celestrak'.format(len(satellites)))
        return satellites

if __name__ == '__main__':
    data = SatelliteTrackService.get_more_satellite_data()
    print(data)
