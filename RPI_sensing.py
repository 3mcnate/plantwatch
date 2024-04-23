# file to collect information from raspberry pi sensor
# sent to mqttPub to be published

import sys
import time
# import grovepi

# adc ref is 5
adc_ref = 5
# set port connections
light_sensor = 0
th_sensor = 1

def main():
    while True:
        gatherData()


# take all readings
def gatherData():
    # light = grovepi.analogRead(light_sensor)
    # humidity, temp = grovepi.analogRead(th_sensor)
    # print(f"Temp: {temp}, Humidity: {humidity}")

    # test values
    temp = 20
    humditiy = 40
    light = 30
    print("gathering data")
    return temp, humditiy, light


if __name__ == "__main__":
    main()
