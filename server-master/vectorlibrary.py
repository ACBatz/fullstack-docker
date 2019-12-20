import numpy as np
import math

center = np.array([0, 0, 0])

def normalize_vector(vector):
    magnitude = np.linalg.norm(vector)
    return vector / magnitude

def get_projection(v_c_p1_hat, v_c_p2_hat, v_c_p3_hat):
    return (v_c_p3_hat * v_c_p1_hat) * v_c_p1_hat + (v_c_p3_hat * v_c_p2_hat) * v_c_p2_hat

def angle_between(v1_hat, v2_hat):
    return np.arccos(np.clip(np.dot(v1_hat, v2_hat), -1.0, 1.0)) * 180 / math.pi

def get_angle_remaining(station1, station2, satellite_position):
    v_c_p1 = station1 - center
    v_c_p2 = station2 - center
    v_c_p3 = satellite_position - center

    v_c_p1_hat = normalize_vector(v_c_p1)
    v_c_p2_hat = normalize_vector(v_c_p2)
    v_c_p3_hat = normalize_vector(v_c_p3)

    angle_s_to_s = angle_between(v_c_p1_hat, v_c_p2_hat)

    proj = get_projection(v_c_p1_hat, v_c_p2_hat, v_c_p3_hat)

    v_c_proj = proj - center
    v_c_proj_hat = normalize_vector(v_c_proj)

    angle_s_to_sat = angle_between(v_c_p1_hat, v_c_proj_hat)

    return angle_s_to_s - angle_s_to_sat