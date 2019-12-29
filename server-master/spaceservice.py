from satellite import Satellite
from threading import Thread


class SatelliteService(Thread):

    def __init__(self, input_file='active.txt', max_sats=-1):
        Thread.__init__(self)
        self.__input_file = input_file
        self.__max_sats = max_sats
        self.__satellites = []

    def get_satellites(self):
        return self.__satellites[:self.__max_sats]

    def run(self):
        self.__generate_data()

    def set_max_sats(self, num):
        if num >= len(self.__satellites) or num <= 0:
            num = -1
        self.__max_sats = num

    def __generate_satellite_data(self):
        print('Parsing active.txt')
        splits = open('active.txt', 'r').readlines()
        print('active.txt parsing complete')
        size = 5
        print('Generating satellites...')
        for i in range(0, len(splits) - 1, 3):
            satellite = Satellite(id=splits[i].replace(' ', '').replace('\n', ''), line1=splits[i+1].replace('\n', ''), line2=splits[i+2].replace('\n', ''), size=size)
            self.__satellites.append(satellite)
        print('Generated {} satellites'.format(len(self.__satellites)))

    def __generate_more_satellite_data(self):
        print('Parsing TLE.txt')
        splits = open('TLE.txt', 'r').readlines()
        print('TLE.txt parsing complete')
        size = 5
        print('Generating satellites...')
        num_lines = self.__max_sats * 2 if self.__max_sats != -1 else len(splits)
        for i in range(0, num_lines - 1, 2):
            satellite = Satellite(id=splits[i].replace('  ', '').split(' ')[2],
                                  line1=splits[i].replace('\n', ''), line2=splits[i + 1].replace('\n', ''),
                                  size=size)
            self.__satellites.append(satellite)
        print('Generated {} satellites'.format(len(self.__satellites)))

    def __generate_data(self):
        if self.__input_file == 'active.txt':
            self.__generate_satellite_data()
        else:
            self.__generate_more_satellite_data()
