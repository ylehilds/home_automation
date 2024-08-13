#!/usr/bin/python
import smtplib
import random
from email.mime.text import MIMEText
import traceback

## Secrets
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

def sendMail(activity):
    fromaddr = config.email["fromaddr"]
    toaddrs  = config.email["toaddrs"]
    
    msg = MIMEText('The Random Activity for the Day is:\n\n' + activity)
    msg['Subject'] = 'The Random Activity for the Day is ...'
    
    # Credentials (if needed)
    username = config.email["username"]
    password = config.email["password"]
    
    # The actual mail send
    server = config.email["server"]
    port = config.email["port"]
    
    try:
        server = smtplib.SMTP(server,port)
        server.ehlo()
        server.starttls()
        server.login(username,password)
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.close()
        print ('successfully sent the activities email')
    except Exception:
        print('failed to send the activities email\n')
        print(traceback.format_exc())

activities_path = os.path.join(os.path.dirname(__file__), 'activities_list.txt')        
with open(activities_path) as f:
    lines = f.readlines()

randomActivity = random.randint(0,len(lines) - 1)

sendMail(lines[randomActivity])
