# subscriber code to collect data from publisher

import paho.mqtt.client as paho
import time
import socket
import pickle
from emailSender import sendEmail

# functions for client object
def on_log(client, userdata, level, buf):
    # print log info when changing connections
    print("log:", buf)


def on_connect(client, userdata, flags, rc, options):
    # connect to broker and subscribe to relevant publishers
    if rc == 0:
        print("Successful connection")
    else:
        print("No connection found")
    client.subscribe("monitor/sensor")


def on_disconnect(client, userdata, flags, rc):
    print("Disconnected, rc:", rc)


# message decoding and sending
def on_message(client, userdata, message):
    
    # decode message
    topic = message.topic
    msg = str(message.payload.decode("utf-8"))
    print("NEW SENSOR READING: " + msg)
    msg = msg.strip().split(' ')
    
    # conver back to int values
    for i in range(3):
        msg[i] = float(msg[i])
    print("Message recieved:", msg)
    
    # write data to file.
    with open("data/sensor.dat", 'w') as datafile:
        datafile.write(str(message.payload.decode("utf-8")))
    
    # email if an alert is needed
    alerts = checkData(msg[0], msg[2], msg[1])
    if len(alerts) != 0:
        sendEmail(msg, alerts)


# # function to check if data outside desired range
def checkData(light, temp, humid):

    with open('data/thresholds.pickle', 'rb') as file:
        thresholds = pickle.load(file)

    light_low = float(thresholds['light-low'])
    light_high = float(thresholds['light-high'])
    temp_low = float(thresholds['temp-low'])
    temp_high = float(thresholds['temp-high'])
    humid_low = float(thresholds['humid-low'])
    humid_high = float(thresholds['humid-high'])

    alerts = []

    if light < light_low or light > light_high:
        alerts.append('l')
        print('LIGHT out of range!')
    if temp < temp_low or temp > temp_high:
        alerts.append('t')
        print('TEMP out of range!')
    if humid < humid_low or humid > humid_high:
        alerts.append('h')
        print('HUMID out of range!')

    return alerts

def start():
    # set broker
    broker = "test.mosquitto.org"

    # create client and connect to broker
    client = paho.Client(paho.CallbackAPIVersion.VERSION2)
    # bind functions to client
    client.on_connect = on_connect
    # client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # connect to broker
    print("Connecting to broker", broker)
    client.connect(broker)

    # start thread to handle requests
    client.loop_start()
