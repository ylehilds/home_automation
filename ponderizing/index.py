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

def sendMail(scripture):
    fromaddr = config.email["fromaddr"]
    toaddrs  = config.email["toaddrs"]
    
    msg = MIMEText('The Ponderizing Scripture for this week is:\n\n' + scripture)
    msg['Subject'] = 'The Ponderizing Scripture for this week is ...'
    
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
        print ('successfully sent the email')
    except Exception:
        print('failed to send the email\n')
        print(traceback.format_exc())
        
scriptures_path = os.path.join(os.path.dirname(__file__), 'scriptures.txt')        
with open(scriptures_path) as f:
    lines = f.readlines()

randomActivity = random.randint(0,len(lines) - 1)

sendMail(lines[randomActivity])
