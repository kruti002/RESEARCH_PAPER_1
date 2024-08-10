import matplotlib.pyplot as plt

def init():
    angles_dict = {
        "armpit_left": 0,
        "armpit_right": 1,
        "elbow_left": 2,
        "elbow_right": 3,
        "hip_left": 4,
        "hip_right": 5,
        "knee_left": 6,
        "knee_right": 7,
        "ankle_left": 8,
        "ankle_right": 9,
    }
    return angles_dict

def error_margin(control, value):
    return control - 20 <= int(value) <= control + 20

def check_joint(angles, joint_name, threshold, body_position):
    angles_dict = init()
    joint_index = angles_dict[joint_name]
    current_angle = angles[joint_index]
    angle_difference = current_angle - threshold
    
    if error_margin(threshold, current_angle):
        return f"Your {joint_name.replace('_', ' ')} is in the right position. Great job!", angle_difference

    deviation = angle_difference
    if deviation > 0:
        return f"Bring your {joint_name.replace('_', ' ')} closer to your {body_position}. Current angle: {current_angle}° (reduce by {abs(deviation)}°).", angle_difference
    else:
        return f"Move your {joint_name.replace('_', ' ')} further from your {body_position}. Current angle: {current_angle}° (increase by {abs(deviation)}°).", angle_difference

    return None, angle_difference

def check_pose_angle(pose_index, angles, df):
    feedback = []
    angle_differences = {}

    joints = ["elbow_right", "elbow_left", "knee_right", "knee_left", "ankle_right", "ankle_left"]
    for joint in joints:
        suggestion, difference = check_joint(angles, joint, int(df.loc[pose_index, joint]), "body" if "elbow" in joint else "leg" if "knee" in joint else "foot")
        if suggestion:
            feedback.append(suggestion)
        angle_differences[joint] = difference

    return feedback, angle_differences
