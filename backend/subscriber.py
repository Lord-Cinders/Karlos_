import math
import paho.mqtt.client as mqtt #import library
from adafruit_servokit import ServoKit

# Servo ports
SHOULDER_RIGHT_ZY = 0
SHOULDER_RIGHT_XY = 1
ELBOW_RIGHT       = 2
SHOULDER_LEFT_ZY = 13
SHOULDER_LEFT_XY = 14
ELBOW_LEFT       = 15

# Default Angles
SRZY = 4
SRXY = 174
SLZY = 180
SLXY = 4

# Networking enums
MQTT_SERVER = "localhost"
MQTT_PATH   = "karlos_brain"

# Base Inputs
prevangles = []
previnputs = [0, 0, 0, 0, 0, 0]

pca = ServoKit(channels = 16)

def init():
    pca.servo[SHOULDER_RIGHT_ZY].angle = SRZY
    pca.servo[SHOULDER_RIGHT_XY].angle = SRXY
    pca.servo[SHOULDER_LEFT_ZY].angle  = SLZY
    pca.servo[SHOULDER_LEFT_XY].angle  = SLXY

def move_servos(angles: list) -> int:
    try:
    # Right hand
        pca.servo[SHOULDER_RIGHT_XY].angle = 180 - angles[0]
        pca.servo[SHOULDER_RIGHT_ZY].angle = angles[1]
        
        # Left hand
        pca.servo[SHOULDER_LEFT_XY].angle  = angles[3]
        pca.servo[SHOULDER_LEFT_ZY].angle  = 180 - angles[4]

    except:
        pass

def smooth_angles(prevangles, angles: list) -> list:
    smoothed = []
    for i in range(len(angles)):
        if angles[i] < prevangles[i]:
            angles[i] = -angles[i]
        smoothedangle = (angles[i] * 0.02) + (prevangles[i] * 0.98) 
        act           = smoothedangle if smoothedangle <= 180 else 180
        smoothed.append(act)
    prevangles = smoothed
    return smoothed

def smooth_controller(prevangles, inputs: list) -> list:
    smoothed = []
    for i in range(len(inputs)):
        smoothedinput = (inputs[i] * 0.98) + (prevangles[i] * 0.02)
        act           = smoothedinput if smoothedinput <= 180 else 180
        smoothed.append(act)
    prevangles = smoothed
    return smoothed 

def move_controller(payload: list):
    steps = 3
    for _ in range(steps):
        try:
            pca.servo[SHOULDER_RIGHT_XY].angle += -(math.floor(payload[0])) / steps
            pca.servo[SHOULDER_RIGHT_ZY].angle += math.floor(payload[1])    / steps
        
        # Left hand
            pca.servo[SHOULDER_LEFT_XY].angle  += math.floor(payload[3])    / steps
            pca.servo[SHOULDER_LEFT_ZY].angle  += -(math.floor(payload[4])) / steps
        except:
            pass
    

def on_connect(client, userdata, flags, rc):
    print("CONNECTION ESTABLISHED "+str(rc))
 
    # Subscribing in oneans that if_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload = str(msg.payload).split(',')
    payload[-1] = payload[-1].rstrip("'")
    mode, payload = payload[0], payload[1:]

    if mode == 'pose':
        payload = list(map(float, payload))
        smoothedangles = smooth_angles(prevangles, payload)
        move_servos(smoothedangles)
    else:
        payload = list(map(float, payload))
        move_controller(payload)
        #payload = smooth_controller(prevangles, payload)
        print(payload)
        #move_servos(smoothedinputs)
        
            


init()
prevangles = [0, 0, 0, 0, 0, 0]
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()
