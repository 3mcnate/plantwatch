# file to collect information from raspberry pi sensor
# sent to mqttPub to be published
import sys
import time
import grovepi
from math import isnan

# adc ref is 5
adc_ref = 5

# set port connections
light_sensor = 0  # analog 0
th_sensor = 2  # digital 2

def main():
    data = gatherData()
    while not dataValid(data):
        data = gatherData()
    print("{0} {1} {2}".format(data[0], data[1], data[2]))

# take all readings
def gatherData():
    [temp, humidity] = grovepi.dht(th_sensor, 0)
    light = grovepi.analogRead(light_sensor)
    return (light, temp, humidity)


# removes erroneous values
def dataValid(data):
    if data[0] > 1000 or data[0] == 0:
        return False
    if isnan(data[1]) or isnan(data[2]):
        return False
    return True


if __name__ == "__main__":
    main()

