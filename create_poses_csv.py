import mediapipe as mp
import pandas as pd
import numpy as np
import cv2
import os

mp_pose = mp.solutions.pose

landmarks_points = {
    "nose": 0,
    "left_shoulder": 11, "right_shoulder": 12,
    "left_elbow": 13, "right_elbow": 14,
    "left_wrist": 15, "right_wrist": 16,
    "left_hip": 23, "right_hip": 24,
    "left_knee": 25, "right_knee": 26,
    "left_ankle": 27, "right_ankle": 28,
    "left_heel": 29, "right_heel": 30,
    "left_foot_index": 31, "right_foot_index": 32,
}

col_names = []
for i in range(len(landmarks_points.keys())):
    name = list(landmarks_points.keys())[i]
    col_names.append(name + "_x")
    col_names.append(name + "_y")
    col_names.append(name + "_z")
    col_names.append(name + "_v")

pose_name = col_names.copy()

pose_name.append("pose")

pose_list = []

main_dir = r'C:\research_paper\research paper\yoga-pose-detection-correction-main\poses_dataset\Images'
pose_dir_list = os.listdir(main_dir)

for i in range(0, len(pose_dir_list)):
    current_path = os.path.join(main_dir, pose_dir_list[i])
    
    # Check if the current path is a directory
    if os.path.isdir(current_path):
        images_dir_list = os.listdir(current_path)
        for l in range(0, len(images_dir_list)):
            pre_list = []
            with mp_pose.Pose(static_image_mode=True, enable_segmentation=True) as pose:
                image = cv2.imread(
                    f"{current_path}/{images_dir_list[l]}")
                result = pose.process(
                    cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

                try:
                    predict = True
                    for landmarks in result.pose_landmarks.landmark:
                        pre_list.append(landmarks)
                except AttributeError:
                    print(
                        f"No points {current_path}/{images_dir_list[l]}")
                    predict = False

            if predict == True:
                gen1116 = np.array([
                    [
                        pre_list[m].x,
                        pre_list[m].y,
                        pre_list[m].z,
                        pre_list[m].visibility
                    ] for m in range(11, 17)
                ]).flatten().tolist()

                gen2333 = np.array([
                    [
                        pre_list[m].x,
                        pre_list[m].y,
                        pre_list[m].z,
                        pre_list[m].visibility
                    ] for m in range(23, 33)
                ]).flatten().tolist()

                gen1116.extend(gen2333)

                all_list = [
                    pre_list[0].x,
                    pre_list[0].y,
                    pre_list[0].z,
                    pre_list[0].visibility,
                ]

                all_list.extend(gen1116)
                tpl = all_list.copy()
                tpl.append(i)
                pose_list.append(tpl)

data_pose = pd.DataFrame(pose_list, columns=pose_name)
data_pose.to_csv("./csv_files/poses_data_pose.csv", index=False)
