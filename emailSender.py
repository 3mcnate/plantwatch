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

    temp = str(data[1])
    humi = str(data[2])
    # convert light level to something better understandable
    light = data[0]
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

def sendEmail(data, alerts):

    sender='plantmonitor741@gmail.com'
    password='jwtvwwlsxzgwyhjn'

    # call function to assemble email
    subject, body = constructEmail(data)

    with open('data/emails.pickle', 'rb') as file:
        emails = pickle.load(file)
    
    addresses = list(emails.keys())
    for address in addresses:

        requested_alerts = emails[address]
        print(f"{address} has requested triggered alerts: {requested_alerts}")

        send = False
        for i in alerts:
            if i in requested_alerts:

                print(f"{address}: sent {i} alert")

                # send email
                send = True
        
        if send:
            message = MIMEText(body)
            message['Subject'] = subject
            message['To'] = address
            message['From'] = sender
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
                smtp_server.login(sender, password)
                smtp_server.sendmail(sender, address, message.as_string())
                print("Message sent!")
