

# # code for raspberry pi
# import paho.mqtt.client as mqtt #import library
# import paho.mqtt.publish as publish
# import amqtt.broker 
# MQTT_SERVER = "localhost"     #specify the broker address, it can be IP of raspberry pi or simply localhost
# MQTT_PATH = "message_channel" #this is the name of topic, like temp
# # # The callback for when the client receives a CONNACK response from the server.
# def on_connect(client, userdata, flags, rc):
#     print("Connected with result code "+str(rc))
#     while(1):
#         message = input()
#         publish.single(MQTT_PATH, message, hostname=MQTT_SERVER)

# # # The callback for when a PUBLISH message is received from the server.
# def on_message(client, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))

 
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message
# client.connect(MQTT_SERVER)
# client.loop_forever()

import telnetlib
host = "192.168.47.1"
port = 8888
timeout = 60
with telnetlib.Telnet(host, port, timeout) as session:
    print("connected?")
    while(True):
        message = input() + '\n'
        if message == "quit\n":
            session.close()
            break
        session.write(message.encode())
