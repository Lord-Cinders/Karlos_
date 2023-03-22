import cv2
import mediapipe as mp
import numpy as np
import time

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
    
cap = cv2.VideoCapture(0)

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
        
        # Extract landmarks
        try:
            landmarks = results.pose_world_landmarks.landmark
            
            # Get coordinates
            hip_xy_right      = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_xy_right  = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_xy_right    = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y ]
            wrist_xy_right    = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y ]
            
            hip_yz_right     = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,       landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            shoulder_yz_right = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            elbow_yz_right    = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]

            hip_xy_left      = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            shoulder_xy_left  = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_xy_left     = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y ]
            wrist_xy_left    = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y ]
            
            hip_yz_left       = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].z,       landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            shoulder_yz_left  = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].z,  landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow_yz_left     = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].z,     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]


            # Calculate Shoulder angle
            Shoulder_angle_xy_right = calculate_angle(hip_xy_right, shoulder_xy_right, elbow_xy_right)
            Shoulder_angle_yz_right = calculate_angle(hip_yz_right, shoulder_yz_right, elbow_yz_right)
            print("Shoulder: ", Shoulder_angle_xy_right, Shoulder_angle_yz_right)
            
            # Calculate elbow angle
            Elbow_angle_xy_right = calculate_angle(shoulder_xy_right, elbow_xy_right, wrist_xy_right)
            Elbow_angle_yz_right = calculate_angle(shoulder_yz_right, elbow_yz_right, wrist_yz_right)
            #print("Elbow: ",Elbow_angle_xy_right, Elbow_angle_yz_right)
            Elbow_angles = str(Elbow_angle_xy_right) + ',' + str(Elbow_angle_yz_right)

            # pushes data into raspberry pi
            #publish.single(MQTT_PATH, str(Shoulder_angle_xy_right) + " " + str(Shoulder_angle_yz_right), hostname=MQTT_SERVER) 

            # Visualize angle
            cv2.putText(image, str(Elbow_angle_yz_right), 
                           tuple(np.multiply(elbow_yz_right, [640, 480]).astype(int)), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                                )
            cv2.putText(image, str(Shoulder_angle_yz_right), 
                           tuple(np.multiply(shoulder_yz_right, [640, 480]).astype(int)), 
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
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()