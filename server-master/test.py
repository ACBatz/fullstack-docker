from multiprocessing import Pool, Process
from spacetrackservice import SatelliteTrackService
from datetime import datetime


def prop(x):
    return x['x'].get_position(x['y'])

def main(o):
    pool = Pool(8)
    results = pool.map(prop, o)
    pool.close()
    pool.join()
    return results

def f(sat):
    return sat['sat'].get_position(sat['time'])

if __name__ == '__main__':
    sats = SatelliteTrackService.get_satellite_data()
    now = datetime.now()
    r = list(map(lambda x: x.get_semi_major_axis(), sats))
    print(r)
    min = min(r)
    max = max(r)
    print('{}:{}'.format(min,max))
