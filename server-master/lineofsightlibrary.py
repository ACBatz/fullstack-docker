import numpy as np

from station import Station
from vectorlibrary import angle_between, normalize_vector, get_angle_remaining
from tree import Tree

center = np.array([0, 0, 0])

def distance_between_points(p0, p1):
    return np.linalg.norm(p0 - p1)

def satellites_have_line_of_sight(s0, s1):
    x0, y0, z0 = s0
    x1, y1, z1 = s1

    earth_radius = 6378137

    midpoint = np.array([(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2])
    return True if distance_between_points(center, midpoint) > earth_radius else False

def station_has_line_of_sight(station_position, satellite_position):
    x0, y0, z0 = station_position
    x1, y1, z1 = satellite_position

    p0 = np.array([x0, y0, z0])
    p1 = np.array([x1, y1, z1])

    v_p0_c = center - p0
    v_p0_p1 = p1 - p0

    v_p0_c_hat = normalize_vector(v_p0_c)
    v_p0_p1_hat = normalize_vector(v_p0_p1)

    return True if angle_between(v_p0_c_hat, v_p0_p1_hat) > 90 else False

def angle_between_stations(s0, s1):
    x0, y0, z0 = s0
    x1, y1, z1 = s1

    p0 = np.array([x0, y0, z0])
    p1 = np.array([x1, y1, z1])

    v_c_p0 = p0 - center
    v_c_p1 = p1 - center

    v_c_p0_hat = normalize_vector(v_c_p0)
    v_c_p1_hat = normalize_vector(v_c_p1)

    return angle_between(v_c_p0_hat, v_c_p1_hat)

def do_routing(origin, destination, satellites, time):
    root = Tree(origin)
    better(origin, destination, root.root, satellites, time)
    return root.get_shortest_path()

def better(origin, destination, node, satellites, time):
    if node.parent and node.data == node.parent.data:
        node.insert(destination, destination)
        return
    elif isinstance(node.data, Station):
        a0 = node.data.get_ecef_position()
        funct = station_has_line_of_sight
    else:
        a0 = node.data.get_propagation(time)
        funct = satellites_have_line_of_sight
    sats = list(filter(lambda x: funct(a0, x.get_propagation(time)), satellites))
    if len(sats) > 0:
        angle, dist = get_best(origin, destination, node.data, sats, time)
        node.insert(angle, dist)
        better(origin, destination, node.left, satellites, time)
        better(origin, destination, node.right, satellites, time)


def get_best(origin, destination, object, satellites, time):
    dest_position = destination.get_ecef_position()
    object_position = object.get_ecef_position() if isinstance(object, Station) else object.get_propagation(time)
    cb = station_has_line_of_sight if isinstance(object, Station) else satellites_have_line_of_sight
    sats = list(filter(lambda x: cb(object_position, x.get_propagation(time)), satellites))
    if object.id == 'uccs':
        print(list(map(lambda x: x.id, sats)))
    best_angle = None
    best_dist = None
    instant_winner = None
    instant_winner_distance = 0
    angle = 360
    dist = 0
    for sat in sats:
        sat_position = sat.get_propagation(time)
        distance = distance_between_points(sat_position, dest_position)
        if station_has_line_of_sight(dest_position, sat_position):
            if not instant_winner:
                instant_winner = sat
                instant_winner_distance = distance
            elif distance < instant_winner_distance:
                instant_winner = sat
                instant_winner_distance = distance
        else:
            theta = get_angle_remaining(origin.get_ecef_position(), dest_position, sat_position)
            if not best_angle:
                best_angle = sat
                angle = theta
            elif theta < angle:
                angle = theta
                best_angle = sat

            if not best_dist:
                best_dist = sat
                dist = distance
            elif distance < dist:
                best_dist = sat
                dist = distance
    if instant_winner:
        return instant_winner, instant_winner
    else:
        return best_angle, best_dist

