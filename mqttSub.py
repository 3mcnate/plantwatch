# subscriber code to collect data from publisher

import paho.mqtt.client as paho
import time
import socket
from emailSender import sendEmail

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
    client.subscribe("monitor/sensor")
def on_disconnect(client, userdata, flags, rc=0):
    print("Disconnected, rc:", rc)

# message decoding and sending
def on_message(client, userdata, message):
    # decode message
    topic = message.topic
    msg = str(message.payload.decode("utf-8"))
    msg = msg.strip().split(',')
    # conver back to int values
    for i in range(3):
        msg[i] = int(msg[i])
    print("Message recieved:", msg)
    # email if an alert is needed
    if checkData(msg):
        sendEmail(msg)


# # function to check if data outside desired range
def checkData(msg, highTemp=50):
    temp = msg[0]
    if temp > highTemp:
        return True
    else: return False


def main():
    # set broker
    broker = "test.mosquitto.org"

    # create client and connect to broker
    client = paho.Client("reciever")
    # bind functions to client
    client.on_connect = on_connect
    # client.on_log = on_log
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # connect to broker
    print("Connecting to broker", broker)
    client.connect(broker, port=1883, keepalive=120)
    client.loop_forever()


if __name__ == "__main__":
    main()
