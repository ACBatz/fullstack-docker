from datetime import datetime

from flask import Flask, render_template, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import math
import json
import pyproj

from lineofsightlibrary import do_routing
from spaceservice import SatelliteService
from station import Station
from timekeeper import TimeKeeper
from singleton import Singleton

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socket = SocketIO(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

singleton = Singleton.get_instance()
singleton.update_data('ecef', pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84'))
singleton.update_data('lla', pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84'))
sat_service = SatelliteService(input_file='TLE.txt')
sat_service.start()


@app.route('/')
def root():
    return render_template('index.html')


@app.route('/trim/<int:num>')
def trim(num):
    sat_service.set_max_sats(num)
    return Response()


def line(sats, station, time):
    min_dist = -1
    closest_sat = None
    for sat in sats:
        dist = distance(sat.get_propagation(time)[0], station.get_ecef_position())
        if min_dist == -1:
            min_dist = dist
            closest_sat = sat
        elif min_dist > dist:
            min_dist = dist
            closest_sat = sat
    return [{'id': '{}|{}'.format(closest_sat.id, station.id)}]


def distance(p_1, p_2):
    return math.sqrt(math.pow(p_1[0] - p_2[0], 2) + math.pow(p_1[1] - p_2[1], 2) + math.pow(p_1[2] - p_2[2], 2))


def get_closest_satellite(sats, station, prop_time):
    min_dist = -1
    closest_sat = None
    for sat in sats:
        dist = distance(sat.get_propagation(prop_time)[0], station.get_ecef_position())
        if min_dist == -1:
            min_dist = dist
            closest_sat = sat
        elif min_dist > dist:
            min_dist = dist
            closest_sat = sat
    return closest_sat, min_dist


def transmit_data(p1, p2, packet_size_bytes, upload_speed_mbps):
    now = time_keeper.get_time()
    if isinstance(p1, Station):
        p1_loc = p1.get_ecef_position()
    else:
        p1_loc = p1.get_propagation(now)[0]

    if isinstance(p2, Station):
        p2_loc = p2.get_ecef_position()
    else:
        p2_loc = p2.get_propagation(now)[0]
    dist = distance(p1_loc, p2_loc)
    latency = dist / 1000 / 300000
    bps = upload_speed_mbps * 125000
    comp_latency = packet_size_bytes / bps
    return latency + comp_latency


uccs = Station('uccs', 38.893601, -104.800619, 0, size=20)
johann = Station('johann', -26.2041, 28.0473, 0, size=20)

lines = []
stations = [uccs, johann]

time_keeper = TimeKeeper()


@app.route('/api/satellite',methods=['POST'])
def satellite():
    try:
        clock_time = request.get_json()['time']
        print('Received POST with jdate of [{}]'.format(clock_time))
        strptime = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_keeper.set_time(strptime)
        start = datetime.now()
        sats_ = list(filter(lambda y: y is not None, map(lambda x: x.get_position(strptime), sat_service.get_satellites())))
        stats_ = list(map(lambda x: x.get_position(), stations))
        stop = datetime.now()
        print('Completed propagation in [{}] seconds and returned [{}] based on filter'.format((stop - start).total_seconds(), len(sats_)))
        res = {'satellites': sats_, 'lines': lines, 'stations': stats_}
        return Response(json.dumps(res), mimetype='application/json')
    except:
        pass
    res = {'satellites': [], 'lines': [], 'stations': []}
    return Response(json.dumps(res), mimetype='application/json')


@socket.on('sim')
def sim():
    global lines
    lines.clear()
    clock_time = time_keeper.get_time()
    print('------Starting routing--------')
    start = datetime.now()
    route, dist = do_routing(uccs, johann, sat_service.get_satellites(), clock_time)
    stop = datetime.now()
    print('------Completed routing in {}s--------'.format((stop - start).total_seconds()))
    lines = route
    socket.emit('sim', {'text': 'Total distance traveled={}'.format(dist)}, broadcast=True)


@socket.on('connect')
def on_connect():
    print('user connected')


if __name__ == '__main__':
    socket.run(app, host='0.0.0.0', port=5000)
