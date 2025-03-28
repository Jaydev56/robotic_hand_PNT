import numpy as np

def calculate_angle(joint_a, joint_b, joint_c):
    vec1 = joint_b - joint_a
    vec2 = joint_c - joint_b
    dot_product = np.dot(vec1, vec2)
    magnitude_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
    angle = np.degrees(np.arccos(np.clip(dot_product / magnitude_product, -1.0, 1.0))) if magnitude_product != 0 else 0
    return angle

def interpolate_servo_angle(angle, input_range, output_range):
    return int(np.clip(np.interp(angle, input_range, output_range), output_range[0], output_range[1]))