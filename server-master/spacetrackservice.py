from satellite import Satellite


class SatelliteTrackService:

    @staticmethod
    def get_satellite_data():
        splits = open('active.txt', 'r').readlines()
        satellites = []
        size = 5
        for i in range(0, len(splits) - 1, 3):
            satellite = Satellite(id=splits[i].replace(' ', '').replace('\n', ''), line1=splits[i+1].replace('\n', ''), line2=splits[i+2].replace('\n', ''), size=size)
            satellites.append(satellite)
        satellites.sort(key=lambda x: x.get_semi_major_axis())
        satellites = satellites[:1250 if len(satellites) >= 1250 else len(satellites)]
        print('Retrieved [{}] satellites from active.txt'.format(len(satellites)))
        return satellites

    @staticmethod
    def get_more_satellite_data():
        print('Parsing TLE.txt')
        splits = open('TLE.txt', 'r').readlines()
        print('TLE.txt parsing complete')
        satellites = []
        size = 5
        print('Generating satellites...')
        for i in range(0, len(splits) - 1, 2):
            satellite = Satellite(id=splits[i].replace('  ', '').split(' ')[2],
                                  line1=splits[i].replace('\n', ''), line2=splits[i + 1].replace('\n', ''),
                                  size=size)
            satellites.append(satellite)
            print('Generated satellite # {}'.format(len(satellites)))
        print('Retrieved [{}] satellites from TLE.txt'.format(len(satellites)))
        return satellites
