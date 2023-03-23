import cv2
import mediapipe as mp
import numpy as np
import time
from controller import XboxController




mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

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



# Network setup      
import paho.mqtt.publish as publish
#webbrowser.open_new_tab("http://172.27.137.89/html")
MQTT_SERVER = "192.168.0.102"
MQTT_PATH = "test_channel"

POSEFLAG = True
CONTROLLERFLAG = False
NETWORKFLAG = False

cap = cv2.VideoCapture(0)
joy = XboxController()
previous_inputs = [0, 0, 0, 0, 0]
current_inputs = [0, 0, 0, 0, 0]
passed_time = time.mktime(time.gmtime())

## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.85, min_tracking_confidence=0.85, model_complexity=2) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # Controller inputs
        current_time = time.mktime(time.gmtime())

        current_inputs = joy.read()
        if current_inputs[-1] == 1 and current_time - passed_time >= 1:
            joy.ControllerFlag *= -1
        
        print(joy.ControllerFlag)

        # Extract landmarks
        try:
            landmarks = results.pose_world_landmarks.landmark
            
            # Get coordinates
            hip_xy_right        = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_xy_right   = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_xy_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y ]
            wrist_xy_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y ]
            
            hip_yz_right        = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_yz_right   = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_yz_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            wrist_yz_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].z,     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y ]

            nose_xyz = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].y, landmarks[mp_pose.PoseLandmark.NOSE.value].z]

            hip_xy_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            shoulder_xy_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
            wrist_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]
            
            hip_yz_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            shoulder_yz_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            wrist_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]

            if(joy.ControllerFlag == -1):
                # Calculate right Shoulder angle
                Shoulder_angle_xy_right = calculate_angle(hip_xy_right, shoulder_xy_right, elbow_xy_right)
                Shoulder_angle_yz_right = calculate_angle(hip_yz_right, shoulder_yz_right, elbow_yz_right)
                print("Right Shoulder: ", Shoulder_angle_xy_right, Shoulder_angle_yz_right)
                Right_Shoulder_angles = str(Shoulder_angle_xy_right) + ',' + str(Shoulder_angle_yz_right)     
                        
                # Calculate right elbow angle
                Elbow_angle_xy_right = calculate_angle(shoulder_xy_right, elbow_xy_right, wrist_xy_right)
                Elbow_angle_yz_right = calculate_angle(shoulder_yz_right, elbow_yz_right, wrist_yz_right)
                print("Right Elbow: ",Elbow_angle_xy_right, Elbow_angle_yz_right)
                Right_Elbow_angles = str(Elbow_angle_xy_right) + ',' + str(Elbow_angle_yz_right)

                # Calculate left Shoulder angle
                Shoulder_angle_xy_left = calculate_angle(hip_xy_left, shoulder_xy_left, elbow_xy_left)
                Shoulder_angle_yz_left = calculate_angle(hip_yz_left, shoulder_yz_left, elbow_yz_left)
                print("Left Shoulder: ", Shoulder_angle_xy_left, Shoulder_angle_yz_left)
                Left_Shoulder_angles = str(Shoulder_angle_xy_left) + ',' + str(Shoulder_angle_yz_left)
                
                # Calculate left elbow angle and nose
                Elbow_angle_xy_left = calculate_angle(shoulder_xy_left, elbow_xy_left, wrist_xy_left)
                Elbow_angle_yz_left = calculate_angle(shoulder_yz_left, elbow_yz_left, wrist_yz_left)
                print("Left Elbow: ",Elbow_angle_xy_left, Elbow_angle_yz_left)
                print("Nose: ", nose_xyz)
                Left_Elbow_angles = str(Elbow_angle_xy_left) + ',' + str(Elbow_angle_yz_left)

            else:
                print(current_inputs)

            
            # pushes data into raspberry pi
            if (joy.ControllerFlag != 1 and NETWORKFLAG):
                publish.single(MQTT_PATH, str(Shoulder_angle_xy_right) + " " + str(Shoulder_angle_yz_right), hostname=MQTT_SERVER) 
            
            elif(joy.ControllerFlag == 1 and NETWORKFLAG):
                publish.single(MQTT_PATH, str(current_inputs), hostname=MQTT_SERVER)

            # Visualize angle
            cv2.putText(image, str(Elbow_angle_yz_right), 
                           tuple(np.multiply(elbow_yz_right, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(Shoulder_angle_yz_right), 
                           tuple(np.multiply(shoulder_yz_right, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(Elbow_angle_xy_left), 
                           tuple(np.multiply(elbow_xy_left, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(Shoulder_angle_xy_left), 
                           tuple(np.multiply(shoulder_xy_left, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(nose_xyz), 
                           tuple(np.multiply(nose_xyz, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            
                  
        except:
            pass
        
        
        # Render detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                 )               
        
        cv2.imshow('Mediapipe Feed', image)
        if cv2.waitKey(10) & 0xFF == ord('q') or current_inputs[4]:
            break
        
        passed_time = current_time 

    cap.release()
    cv2.destroyAllWindows()