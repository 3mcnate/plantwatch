# publisher code to post to sub

import paho.mqtt.client as paho
import time
import socket
import subprocess
import os

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


def get_data():
    # Create a list of arguments to pass to the Python 2 program
    command = ["/usr/bin/python", "get_data.py"]

    # Run the get_data python script
    finished_process = subprocess.run(command, capture_output=True, text=True)
    return finished_process.stdout.strip()


def main():

    # set broker
    broker = "test.mosquitto.org"

    # create client and connect to broker
    client = paho.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect

    client.connect(broker, port=8081, keepalive=120)
    client.loop_start()
    time.sleep(1)

    while True:
        data = get_data()
        print("GrovePi readings: " + data)
        print("Publishing to MQTT.")
        client.publish("monitor/sensor", data)
        time.sleep(1)
        

    


if __name__ == "__main__":
    main()
