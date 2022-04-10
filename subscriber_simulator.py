import paho.mqtt.client as mqtt
import time
import json
import datetime
from connection import *

# Callback function - executed when the program successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

#Callback function - executed when the program gracefully disconnects from the broker
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

#Callback function - executed whenever a message is published to the topics that
#this program is subscribed to
def on_message(client, userdata, msg):
    # print(msg.topic, str(msg.payload), "retain", msg.retain, "qos", msg.qos, str(userdata) )
    data = msg.payload.decode('utf-8')
    data = json.loads(data)
    device_id = data["device_id"]
    location = data["location"]
    temperature = data["temperature"]
    humidity = data["humidity"]
    pressure = data["pressure"]
    # reading_time = data["reading_time"]
    reading_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    create_device_data(device_id, location, temperature, humidity, pressure, reading_time)

#Defining an MQTT client object
client = mqtt.Client()

#Setting callback functions for various client operations
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

#Reading the configuration file
f=open("config-sub.json")
config = json.loads(f.read())
f.close()

# Initialising devices from the config.json file and assigning device_ids to each device
device_config = []
for device in config['devices']:
    # dev = {}
    # dev['device_id'] = device['device_id']
    # dev['publish_frequency'] = device['publish_frequency']
    # dev['location'] = device['location']
    # dev['temperature_std_val'] = device['temperature_std_val']
    # dev['humidity_std_val'] = device['humidity_std_val']
    # dev['pressure_std_val'] = device['pressure_std_val']
    # dev['publish_topic'] = device['publish_topic']
    # device_config.append(dev)
    # Create the each device in the devices table
    create_device(device['device_id'], device['description'])


#Connecting to broker
client.connect(host=config["broker_host"], port=config["broker_port"], keepalive=60)

'''
Start the MQTT client non-blocking loop to listen the broker for messages
in subscribed topics and other operations for which the callback functions
are defined
'''
client.loop_start()

for device in config['devices']:
    # if clock % device['publish_frequency'] == 0:
        print("Subscribed to topic " + device["publish_topic"])
        #Subscribe to the topic
        client.subscribe(device["publish_topic"])

while True:
    try:
        # Iterating through the items in device configuration dictionary, every second
        time.sleep(1)

    #Disconnect the client from MQTT broker and stop the loop gracefully at
    # Keyboard interrupt (Ctrl+C)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break
