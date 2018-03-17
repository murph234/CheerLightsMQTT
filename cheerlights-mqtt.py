#!/usr/bin/env python

#
# CheerLights is an interactive IoT project by Hans Scharler at www.cheerlights.com
# This client is designed for the Raspberry Pi using the Pimoroni Blinkt! shim for display
# and MQTT to subscribe to the CheerLights feed at Thingspeak.
#
import paho.mqtt.client as mqtt
import random
import time
import json
from sys import exit
import blinkt

# The Hostname of the ThingSpeak MQTT broker.
mqttHost = "mqtt.thingspeak.com"

# You can use any Username.
mqttUsername = "CheerLightsMQTT"

# Your MQTT API Key from Account > My Profile.
mqttAPIKey ="XXXXXXXXXXXXXXXX"

# Array of colors
colors = ['000000','000000','000000']
# LED count (using the Pimoroni Blinkt!)
numLEDs = 8

# Setup various callback functions for mqtt events
def on_connect(mqttc, obj, flags, rc):
    print("Connected to %s:%s" % (mqttc._host, mqttc._port))

def on_message(mqttc, obj, msg):
	global colors
# Load the json response into a dictionary
	message = json.loads(msg.payload)
# Grab the hex color value and strip off the leading '#'
	color = message['field2'].lstrip('#')
# Add the new one to the list and drop the oldest one
	colors.append(color)
	colors.pop(0)
	print(message['status'])

def on_publish(mqttc, obj, mid):
    print("mid: " + str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)

# If you want to use a specific client id, use
# mqttc = mqtt.Client("client-id")
# but note that the client id must be unique on the broker. Leaving the client
# id parameter empty will generate a random id for you.
mqttc = mqtt.Client()
# Set the callback functions
mqttc.username_pw_set(mqttUsername,mqttAPIKey)
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_publish = on_publish
mqttc.on_subscribe = on_subscribe
# Uncomment to enable debug messages
#mqttc.on_log = on_log
# Connect to the mqtt server and subscribe to the Cheerlights channel
mqttc.connect(mqttHost, 1883, 60)
mqttc.subscribe("channels/1417/subscribe/json", 0)

# Start a background loop to receive mqtt messages
mqttc.loop_start()

while True:
	# Pick a random pixel and set it to a random color from the list
	i = random.randint(0,numLEDs - 1)
	r, g, b = bytearray.fromhex(random.choice(colors))
	blinkt.set_pixel(i, r, g, b)
	blinkt.show()
	time.sleep(0.01)
