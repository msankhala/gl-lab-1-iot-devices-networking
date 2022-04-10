import paho.mqtt.client as mqtt
import time
import json
import numpy as np
import datetime
from connection import *

# Callback function - executed when the program successfully connects to the broker
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # client.subscribe("devices/weather")

#Callback function - executed when the program gracefully disconnects from the broker
def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

#Defining an MQTT client object
client = mqtt.Client()

#Setting callback functions for various client operations
client.on_connect = on_connect
client.on_disconnect = on_disconnect

#Reading the configuration file
f=open("config-new.json")
config = json.loads(f.read())
f.close()

# Initialising devices from the config.json file and assigning device_ids to each device
device_config = []
for device in config['devices']:
    dev = {}
    dev['device_id'] = device['device_id']
    dev['publish_frequency'] = device['publish_frequency']
    dev['location'] = device['location']
    dev['temperature_std_val'] = device['temperature_std_val']
    dev['humidity_std_val'] = device['humidity_std_val']
    dev['pressure_std_val'] = device['pressure_std_val']
    dev['publish_topic'] = device['publish_topic']
    device_config.append(dev)
    # Create the each device in the devices table
    # create_device(device['device_id'])


#Connecting to broker
client.connect(host=config["broker_host"], port=config["broker_port"], keepalive=60)

'''
Start the MQTT client non-blocking loop to listen the broker for messages
in subscribed topics and other operations for which the callback functions
are defined
'''
client.loop_start()

clock=0
while True:
    try:
        # Iterating through the items in device configuration dictionary, every second
        time.sleep(1)
        clock = clock+1
        for device in device_config:
            if clock % device['publish_frequency'] == 0:
                print("Published to topic " + device["publish_topic"])
                #Initialize a dictionary to be sent as publish message
                message = {}
                #Generate timestamp in YYYY-MM-DD HH:MM:SS format
                message["reading_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message["device_id"] = device["device_id"]
                message["location"] = device["location"]
                #Generate a random value using normal distribution function of the
                # configured standard value
                message["temperature"] = round(np.random.normal(device["temperature_std_val"],2),2)
                message["humidity"] = round(np.random.normal(device["humidity_std_val"],2),2)
                message["pressure"] = round(np.random.normal(device["pressure_std_val"],2),2)
                #Publish the message
                client.publish(device["publish_topic"], json.dumps(message))

    #Disconnect the client from MQTT broker and stop the loop gracefully at
    # Keyboard interrupt (Ctrl+C)
    except KeyboardInterrupt:
        client.disconnect()
        client.loop_stop()
        break
