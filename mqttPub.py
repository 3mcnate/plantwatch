# publisher code to post to sub

import paho.mqtt.client as paho
import time
import socket
from RPI_sensing import *

# NOTE: most of the code is similar in structure to mqttPub.py
def on_log(client, userdata, level, buf):
    print("log:", buf)
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successful connection")
    else:
        print("No connection found")
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected, rc:", rc)


def main():
    # set broker
    broker = "test.mosquitto.org"

    # create client and connect to broker
    client = paho.Client("monitor")
    client.on_connect = on_connect
    # client.on_log = on_log
    client.on_disconnect = on_disconnect
    print("Connecting to broker", broker)
    client.connect(broker, port=1883, keepalive=120)
    client.loop_start()
    time.sleep(1)

    data = 0
    # run publish loop indefinitely as data is received
    while True:
        # pull data from rpi and post to server
        temp, humi, light = gatherData()
        data = f"Temp: {temp}\nHumidity: {humi}\nLight: {light}"
        client.publish("monitor/sensor", data)
        time.sleep(4)


if __name__ == "__main__":
    main()
