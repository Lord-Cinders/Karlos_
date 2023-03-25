import paho.mqtt.client as mqtt #import library
from adafruit_servokit import ServoKit

# Servo ports
SHOULDER_RIGHT_ZY = 0
SHOULDER_RIGHT_XY = 1
ELBOW_RIGHT       = 2
SHOULDER_LEFT_ZY = 14
SHOULDER_LEFT_XY = 13
ELBOW_LEFT       = 15

# Default Angles
SRZY = 0
SRXY = 180
SLZY = 180
SLXY = 0

# Networking enums
MQTT_SERVER = "localhost"
MQTT_PATH   = "karlos_arms"

# Base Inputs
prevangles = [0, 0, 0, 0, 0, 0]
previnputs = [0, 0, 0, 0, 0, 0]

pca = ServoKit(channels = 16)

def init():
    pca.servo[SHOULDER_RIGHT_ZY].angle = SRZY
    pca.servo[SHOULDER_RIGHT_XY].angle = SRXY
    pca.servo[SHOULDER_LEFT_ZY].angle  = SLZY
    pca.servo[SHOULDER_LEFT_XY].angle  = SLXY

def move_servos(angles: list) -> int:

    # Right hand
    pca.servo[SHOULDER_RIGHT_XY].angle = angles[0]
    pca.servo[SHOULDER_RIGHT_ZY].angle = angles[1]
    
    # Left hand
    pca.servo[SHOULDER_LEFT_XY].angle  = angles[3]
    pca.servo[SHOULDER_LEFT_ZY].angle  = angles[4]


def smooth_angles(angles: list) -> list:
    smoothed = []
    for i in range(len(angles)):
        if angles[i] < prevangles[i]:
            angles[i] = -angles[i]
        smoothedangle = (angles[i] * 0.02) + (prevangles[i] * 0.98)
        smoothed.append(smoothedangle)
    prevangles = smoothed
    return smoothed

def smooth_controller(inputs: list) -> list:
    smoothed = []
    for i in range(len(input)):
        smoothedinput = (input[i] * 0.02) + (prevangles[i] * 0.98)
        smoothed.append(smoothedinput)
    prevangles = smoothed
    return smoothed



def on_connect(client, userdata, flags, rc):
    print("CONNECTION ESTABLISHED "+str(rc))
 
    # Subscribing in oneans that if_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload = msg.payload.split(',')
    if payload[0] == 'pose':
        smoothedangles = smooth_angles(payload[1:])
        move_servos(smoothedangles)
    else:
        smoothedinputs = smooth_controller(payload[1:])
        move_servos(smoothedinputs)


init()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()
