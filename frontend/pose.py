import numpy as np

#calculating the angle
def calculate_angle(a,b,c):
    a = np.array(a) # First
    b = np.array(b) # Mid
    c = np.array(c) # End
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle
        
    return angle 

def pose_paylaod(THREEDMODE: bool, results, mp_pose):

    # Extract landmarks
        try:
            landmarks = results.pose_world_landmarks.landmark
            
            # Get coordinates
            # Right Hand
            hip_xy_right        = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_xy_right   = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_xy_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y ]
            wrist_xy_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y ]
            
            hip_yz_right        = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_yz_right   = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_yz_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_yz_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z,     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

            # Left Hand
            hip_xy_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ]
            shoulder_xy_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,   landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]
            elbow_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,      landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
            wrist_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,      landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y  ]
            
            hip_yz_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z ,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y ] 
            shoulder_yz_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y ]
            elbow_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z ,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]
            wrist_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z ,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y  ]

            
            # Calculate right Shoulder angle
            Shoulder_angle_xy_right = str(calculate_angle(hip_xy_right, shoulder_xy_right, elbow_xy_right))
            Shoulder_angle_yz_right = str(calculate_angle(hip_yz_right, shoulder_yz_right, elbow_yz_right))
            #print("Right Shoulder: ", Shoulder_angle_xy_right, Shoulder_angle_yz_right)
            Right_Shoulder_angles   = str(Shoulder_angle_xy_right) + ',' + str(Shoulder_angle_yz_right)     
                    
            # Calculate right elbow angle
            Elbow_angle_xy_right = str(calculate_angle(shoulder_xy_right, elbow_xy_right, wrist_xy_right))
            Elbow_angle_yz_right = str(calculate_angle(shoulder_yz_right, elbow_yz_right, wrist_yz_right))
            #print("Right Elbow: ",Elbow_angle_xy_right, Elbow_angle_yz_right)
            Right_Elbow_angles   = str(Elbow_angle_xy_right) + ',' + str(Elbow_angle_yz_right)

            # Calculate left Shoulder angle
            Shoulder_angle_xy_left = str(calculate_angle(hip_xy_left, shoulder_xy_left, elbow_xy_left))
            Shoulder_angle_yz_left = str(calculate_angle(hip_yz_left, shoulder_yz_left, elbow_yz_left))
            #print("Left Shoulder: ", Shoulder_angle_xy_left, Shoulder_angle_yz_left)
            Left_Shoulder_angles   = str(Shoulder_angle_xy_left) + ',' + str(Shoulder_angle_yz_left)
            
            # Calculate left elbow angle and nose
            Elbow_angle_xy_left = str(calculate_angle(shoulder_xy_left, elbow_xy_left, wrist_xy_left))
            Elbow_angle_yz_left = str(calculate_angle(shoulder_yz_left, elbow_yz_left, wrist_yz_left))
            #print("Nose: ", nose_xyz)
            Left_Elbow_angles   = str(Elbow_angle_xy_left) + ',' + str(Elbow_angle_yz_left)
            if THREEDMODE:
                payload = "pose3," + Right_Shoulder_angles + ',' + Elbow_angle_yz_right + ',' +Left_Shoulder_angles + ',' + Elbow_angle_yz_left
            else:
                payload = "pose2," + Right_Shoulder_angles + ',' + Elbow_angle_xy_right + ',' +Left_Shoulder_angles + ',' + Elbow_angle_xy_left
    
            return payload
        except:
              return -1
