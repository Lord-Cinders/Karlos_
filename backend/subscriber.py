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

def on_connect(client, userdata, flags, rc):
    print("CONNECTION ESTABLISHED "+str(rc))
 
    # Subscribing in oneans that if_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PATH)

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))
    payload = msg.payload.split(',')
    if payload[0] == 'pose':
        pass
    else:
        pass


init()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER)
client.loop_forever()
