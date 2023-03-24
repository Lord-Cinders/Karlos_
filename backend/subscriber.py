import paho.mqtt.client as mqtt #import library
from adafruit_servokit import ServoKit

# Servo ports
SHOULDER_RIGHT_XY = 0
SHOULDER_RIGHT_ZY = 1
ELBOW_RIGHT       = 2

SHOULDER_LEFT_XY = 13
SHOULDER_LEFT_ZY = 14
ELBOW_LEFT       = 15

# Networking enums
MQTT_SERVER = "localhost"
MQTT_PATH   = "karlos_arms"

pca = ServoKit(channels = 16)

def init():
    pass

def move_servos(angles):
    pass
