# file used to send email given information from pi

import smtplib
from email.mime.text import MIMEText
import pickle

# user credentials
sender = "plantmonitor741@gmail.com"
password = 'jwtvwwlsxzgwyhjn'
receiver = "nboxer@usc.edu"

# function takes in data from RPI and makes email
def constructEmail(data):
    subject = "ALERT: Your plants need your help!"

    temp = str(data[0])
    humi = str(data[1])
    # convert light level to something better understandable
    light = data[2]
    if light < 200:
        lightLevel = "DARK"
    elif light > 600:
        lightLevel = "TOO BRIGHT"
    else:
        lightLevel = "NORMAL"

    body = f"""
    You need to save your plants! It appears as though your plants are in an environment that might be harmful. Here's what our sensor found:
    Current Temperature: {temp}
    Current Humidity: {humi}
    Light Level: {lightLevel}
    """
    return subject, body

def sendEmail(data, receiver='blackadarj22@icloud.com', sender='plantmonitor741@gmail.com', password='jwtvwwlsxzgwyhjn'):
    # call function to assemble email
    subject, body = constructEmail(data)

    message = MIMEText(body)
    message['Subject'] = subject
    message['To'] = receiver
    message['From'] = sender
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, receiver, message.as_string())
    print("Message sent!")
