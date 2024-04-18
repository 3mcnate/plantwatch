# client code to collect data from publisher

import paho.mqtt.client as paho
import time

# functions for client object
def on_log(client, userdata, level, buf):
    # print log info when changing connections
    print("log:", buf)
def on_connect(client, userdata, flags, rc):
    # connect to broker and subscribe to relevant publishers
    if rc == 0:
        print("Successful connection")
    else:
        print("No connection found")
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected, rc:", rc)


# message decoding
def on_message(client, userdata, message):
    # print the message whenever recieved from the publisher
    topic = message.topic
    decoded_msg = str(message.payload.decode("utf-8"))
    print("Message recieved:", decoded_msg)


# set broker
broker = "test.mosquitto.org"

# create client and connect to broker
client = paho.Client("monitor")
# bind functions to client
client.on_connect = on_connect
# client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_message = on_message

# connect to broker
print("Connecting to broker", broker)
client.connect(broker)
client.loop_start()

# publish message
client.subscribe("house/sensor1")
client.publish("house/sensor1", "?")

time.sleep(4)

client.loop_stop()
client.disconnect()