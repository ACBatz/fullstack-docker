from multiprocessing import Process
from spacetrackservice import SatelliteTrackService
from datetime import datetime
from satellite import Satellite


if __name__ == '__main__':
    sats = SatelliteTrackService.get_satellite_data()
    start = datetime.now()
    sats_ = list(filter(lambda y: y is not None, map(lambda x: x.get_position(start), sats)))
    stop = datetime.now()
    print((stop - start).seconds)
    p = Process(target=Satellite.get_static_position, args=(, start))
    p.start()
    p.join()