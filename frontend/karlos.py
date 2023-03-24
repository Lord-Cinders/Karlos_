import cv2
import mediapipe as mp
import time
import webbrowser
import paho.mqtt.publish as publish
from pose import pose_paylaod
from cli import parse_argv
from controller import XboxController


def karlos(sys):
    # Default ENUMS
    POSEFLAG        = True
    CONTROLLERFLAG  = False
    NETWORKFLAG     = False
    CAMERAFLAG      = False
    MQTTSERVER      = ""
    MQTTPATH        = "test_channel"

    data = parse_argv(sys)
    if data == None and len(sys.argv) > 1:
        return 
    if(data != None):
        CONTROLLERFLAG  = data["CONTROLLERFLAG"] == "True"
        NETWORKFLAG     = data["NETWORKFLAG"]    == "True"
        CAMERAFLAG      = data["CAMERAFLAG"]     == "True"
        MQTTSERVER      = data["MQTTSERVER"].strip('\"')
        MQTTPATH        = data["MQTTPATH"].strip('\"')
    
    
    # Network setup      
    if(NETWORKFLAG and CAMERAFLAG):
        webbrowser.open_new_tab("http://172.27.137.89/html")

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)
    joy = XboxController()
    payload = ""
    current_inputs = [0, 0, 0, 0, 0]
    passed_time = time.mktime(time.gmtime())

    if(CONTROLLERFLAG):
        joy.ControllerFlag = 1     
    
    ## Setup mediapipe instance
    with mp_pose.Pose(min_detection_confidence=0.85, min_tracking_confidence=0.85, model_complexity=2) as pose:
        while cap.isOpened():

            current_time = time.mktime(time.gmtime())
            # Controller inputs
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

            if(joy.ControllerFlag == -1):
                payload = pose_paylaod(results, mp_pose)
            
            if( payload == - 1 or joy.ControllerFlag == 1):
                payload = joy.calculate_payload(current_inputs)
                
            print(payload)

            # Render detections
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                            mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=2), 
                                            mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2) 
                                            )               
            cv2.imshow('Mediapipe Feed', image)
            if cv2.waitKey(10) & 0xFF == ord('q') or current_inputs[-1]:
                break

            # pushes data into raspberry pi
            if (NETWORKFLAG and current_time - passed_time >= 1):
                publish.single(MQTTPATH, payload, hostname=MQTTSERVER) 
        
            passed_time = current_time 

        cap.release()
        cv2.destroyAllWindows()