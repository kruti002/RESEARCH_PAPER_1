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
    if error_margin(threshold, current_angle):
        return f"Your {joint_name.replace('_', ' ')} is in the right position. Great job!"

    deviation = current_angle - threshold
    if deviation > 0:
        return f"Bring your {joint_name.replace('_', ' ')} closer to your {body_position}. Current angle: {current_angle}° (reduce by {abs(deviation)}°)."
    else:
        return f"Move your {joint_name.replace('_', ' ')} further from your {body_position}. Current angle: {current_angle}° (increase by {abs(deviation)}°)."

    return None

def check_pose_angle(pose_index, angles, df):
    feedback = []
    feedback.append(check_joint(angles, "elbow_right", int(df.loc[pose_index, "elbow_right"]), "body"))
    feedback.append(check_joint(angles, "elbow_left", int(df.loc[pose_index, "elbow_left"]), "body"))
    feedback.append(check_joint(angles, "knee_right", int(df.loc[pose_index, "knee_right"]), "leg"))
    feedback.append(check_joint(angles, "knee_left", int(df.loc[pose_index, "knee_left"]), "leg"))
    feedback.append(check_joint(angles, "ankle_right", int(df.loc[pose_index, "ankle_right"]), "foot"))
    feedback.append(check_joint(angles, "ankle_left", int(df.loc[pose_index, "ankle_left"]), "foot"))

    return [message for message in feedback if message is not None]
