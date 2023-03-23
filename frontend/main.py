import cv2
import mediapipe as mp
import numpy as np
import time
import sys
import re
from controller import XboxController
import paho.mqtt.publish as publish

POSEFLAG = True
CONTROLLERFLAG = False
NETWORKFLAG = False
MQTTSERVER = ""
MQTTPATH = "test_channel"

if(len(sys.argv) > 1):
    if (sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print("Available arguements:")
        print("-n [ip of subscriber]          | -n <local>        : sets the ip address of the pi subscriber    <default: runs on local>")
        print("--network [ip of subscriber]   | --network <local> : sets the ip address of the pi subscriber    <default: runs on local>")
        print("-s <controller>                | -s <pose>         : sets the control    <default: runs with controller>")
        print("-start <controller>            | -start <pose>     : sets the control    <default: runs with controller>")
        print("-f /path/to/file                                   : reads config data from a file")
        print("-file /path/to/file                                : reads config data from a file")


    if(sys.argv.count('-n') == 1 or sys.argv.count('--network') == 1):
    
        ipexp = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        try:
            arg_index = sys.argv.index('-n') 
        except:
            arg_index = sys.argv.index('--network') 

        NETWORKFLAG = True if ( sys.argv[arg_index + 1] != 'local' and re.search(ipexp, sys.argv[arg_index + 1])) else False
        MQTTSERVER = sys.argv[arg_index + 1]
        print("your subscriber ip has been set to:", (sys.argv[arg_index + 1]))

    if(sys.argv.count('-s') == 1 or sys.argv.count('--start') == 1):
        try:
            arg_index = sys.argv.index('-s') 
        except:
            arg_index = sys.argv.index('--start') 

        CONTROLLERFLAG = True if ( sys.argv[arg_index + 1] == 'controller') else False
        print("your default control has been set to:", (sys.argv[arg_index + 1]))        

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

#webbrowser.open_new_tab("http://172.27.137.89/html")




cap = cv2.VideoCapture(0)
joy = XboxController()

if(CONTROLLERFLAG):
    joy.ControllerFlag = 1     

previous_inputs = [0, 0, 0, 0, 0]
current_inputs = [0, 0, 0, 0, 0]
passed_time = time.mktime(time.gmtime())
payload = ""
## Setup mediapipe instance
with mp_pose.Pose(min_detection_confidence=0.85, min_tracking_confidence=0.85, model_complexity=2) as pose:
    while cap.isOpened():
        # Controller inputs
        current_time = time.mktime(time.gmtime())

        current_inputs = joy.read()
        if current_inputs[-2] == 1 and current_time - passed_time >= 1:
            joy.ControllerFlag *= -1

        ret, frame = cap.read()
        
        # Recolor image to RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
      
        # Make detection
        results = pose.process(image)
    
        # Recolor back to BGR
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        #print(joy.ControllerFlag)
        if(joy.ControllerFlag == -1):
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

                nose_xyz = [landmarks[mp_pose.PoseLandmark.NOSE.value].x, landmarks[mp_pose.PoseLandmark.NOSE.value].z, landmarks[mp_pose.PoseLandmark.NOSE.value].y]

                hip_xy_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                shoulder_xy_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
                wrist_xy_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]
                
                hip_yz_left         = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                shoulder_yz_left    = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
                wrist_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].z,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]

                
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

                payload = Right_Shoulder_angles + ',' + Elbow_angle_yz_right + ',' +Left_Shoulder_angles + ',' + Elbow_angle_yz_left

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
                # Render detections
                
            
                
            except:
                pass
        
        else:
                #print(current_inputs)
                shoulder_left_dxy   = str(current_inputs[0]     // 12)                       # Normalize to -11 to 10
                shoulder__left_dzy  = str(current_inputs[1]     // 12)                       # Normalize to -11 to 10
                elbow_left          = str((current_inputs[2]    // 25) * -current_inputs[3]) # Normalize to -10 to 10
                shoulder_right_dxy  = str(current_inputs[4]     // 12)                       # Normalize to -11 to 10
                shoulder_right_dzy  = str(current_inputs[5]     // 12)                       # Normalize to -11 to 10
                elbow_right         = str((current_inputs[6]    // 25) * -current_inputs[7]) # Normalize to -10 to 10
                
                payload = shoulder_right_dxy + ',' + shoulder_right_dzy + ',' + elbow_right + ',' + shoulder_left_dxy + ',' + shoulder__left_dzy + ',' + elbow_left
            
        print(payload)
        cv2.imshow('Mediapipe Feed', image)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                        mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                        mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                        )               
        
        if cv2.waitKey(10) & 0xFF == ord('q') or current_inputs[-1]:
            break

        # pushes data into raspberry pi
            if (joy.ControllerFlag != 1 and NETWORKFLAG):
                publish.single(MQTTPATH, payload, hostname=MQTTSERVER) 
            
            elif(joy.ControllerFlag == 1 and NETWORKFLAG):
                publish.single(MQTTPATH, payload, hostname=MQTTSERVER)

        passed_time = current_time 

    cap.release()
    cv2.destroyAllWindows()