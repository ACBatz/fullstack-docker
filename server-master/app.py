from datetime import datetime

from flask import Flask, render_template, Response, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import logging
import math
import json

from lineofsightlibrary import do_routing
from spacetrackservice import SatelliteTrackService
from station import Station
from timekeeper import TimeKeeper

app = Flask(__name__)
app.config['SECRET_KEY'] = 'development key'
socket = SocketIO(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})
# logging.basicConfig(filename='satellite.log', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
@app.route('/')
def hello_world():
    return render_template('index.html')

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

sats = []
lines = []
stations = [uccs, johann]

time_keeper = TimeKeeper()

@app.route('/api/satellite',methods=['POST'])
def satellite():
    global sats
    if len(sats) == 0:
        sats = SatelliteTrackService.get_satellite_data()
    try:
        clock_time = request.get_json()['time']
        print('Received POST with jdate of [{}]'.format(clock_time))
        strptime = datetime.strptime(clock_time, '%Y-%m-%dT%H:%M:%S.%f%z')
        time_keeper.set_time(strptime)
        start = datetime.now()
        sats_ = list(filter(lambda y: y is not None, map(lambda x: x.get_position(strptime), sats)))
        stats_ = list(map(lambda x: x.get_position(), stations))
        stop = datetime.now()
        print('Completed propagation in [{}] seconds and returned [{}] based on filter'.format((stop - start).total_seconds(), len(sats_)))
        res = {'satellites': sats_, 'lines': lines, 'stations': stats_}
        return Response(json.dumps(res), mimetype='application/json')
    except:
        pass
    res = {'satellites': [], 'lines': [], 'stations': []}
    return Response(json.dumps(res), mimetype='application/json')
i = 0
@socket.on('sim')
def sim():
    global lines
    lines.clear()
    clock_time = time_keeper.get_time()
    print('------Starting routing--------')
    start = datetime.now()
    route, dist = do_routing(uccs, johann, sats, clock_time)
    stop = datetime.now()
    print('------Completed routing in {}s--------'.format((stop - start).total_seconds()))
    lines = route
    socket.emit('sim', {'text': 'Total distance traveled={}'.format(dist)}, broadcast=True)

    # socket.emit('sim', {'text': 'Calculating optimum path...'}, broadcast=True)
    # closest_sat_to_host, host_dist = get_closest_satellite(sats, uccs, clock_time)
    # lines.append({'id': '{}|{}'.format(closest_sat_to_host.id, uccs.id)})
    # closest_sat_to_dest, dest_dist = get_closest_satellite(sats, johann, clock_time)
    # lines.append({'id': '{}|{}'.format(closest_sat_to_dest.id, johann.id)})
    # lines.append({'id': '{}|{}'.format(closest_sat_to_host.id, closest_sat_to_dest.id)})
    # sat_to_sat_dist = distance(closest_sat_to_host.get_propagation(clock_time)[0], closest_sat_to_dest.get_propagation(clock_time)[0])
    # socket.emit('sim', {'text': 'Optimum path found:'}, broadcast=True)
    # socket.emit('sim', {'text': 'UCCS to {} - Distance={}'.format(closest_sat_to_host.id, host_dist / 1000)}, broadcast=True)
    # socket.emit('sim', {'text': '{} to {} - Distance={}'.format(closest_sat_to_host.id, closest_sat_to_dest.id, sat_to_sat_dist / 1000)}, broadcast=True)
    # socket.emit('sim', {'text': '{} to Johannesburg, SA - Distance={}'.format(closest_sat_to_dest, dest_dist / 1000)}, broadcast=True)
    # socket.emit('sim', {'text': 'Total Trip Distance= {}'.format((host_dist + sat_to_sat_dist + dest_dist) / 1000)}, broadcast=True)
    # time.sleep(1)
    # socket.emit('sim', {'text': 'Initiating ping between UCCS and Johannesburg, South Africa'}, broadcast=True)
    # time.sleep(1)
    # socket.emit('sim', {'text': 'Pinging 41.134.5.66 with 32 bytes of data:'}, broadcast=True)
    # l1 = transmit_data(uccs, closest_sat_to_host, 32, 250)
    # socket.emit('sim', {'text': 'Pinging 41.134.5.66 with 32 bytes of data:'}, broadcast=True)



@socket.on('connect')
def on_connect():
    print('user connected')

if __name__ == '__main__':
    socket.run(app)
