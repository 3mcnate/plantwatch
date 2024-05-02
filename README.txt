Team:
Nate Boxer
Jack Blackadar

Instructions:
1. Install GrovePi shield on the Raspberry Pi
2. Install light sensor on port A0
3. Install temp/humidity sensor on port D2
4. SSH into Rpi and copy the pi_code folder over.
5. Run "python3 mqttPub.py" on the Rpi
6. On the server computer, run "python3 server.py"
7. Open the frontend at localhost:5000 and enjoy

Libraries used:
1. Flask
2. Paho MQTT
3. GrovePi Python library
4. Python Pickle