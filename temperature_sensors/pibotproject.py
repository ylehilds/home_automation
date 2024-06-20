#!/usr/bin/python

import re
import time
import json
import psutil
import requests
from subprocess import call
from slackclient import SlackClient

## Secrets
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

slack_client = SlackClient(config.slack['slack_client'])
API_ENDPOINT = config.aws['sensors_server_ip_address'] + "/relay"
API_ENDPOINT_BASEMENT = config.aws['sensors_server_ip_address'] + "/temperature/basement"
API_ENDPOINT_MAIN = config.aws['sensors_server_ip_address'] + "/temperature/main"
API_ENDPOINT_UPSTAIRS = config.aws['sensors_server_ip_address'] + "/temperature/upstairs"
FAN_STATE = 'OFF'
# Fetch your Bot's User ID
user_list = slack_client.api_call("users.list")
for user in user_list.get('members'):
    if user.get('name') == "pibotproject":
        slack_user_id = user.get('id')
        break


# Start connection
if slack_client.rtm_connect(with_team_state=False):
    print ("Connected!")

    while True:
        for message in slack_client.rtm_read():
            if 'text' in message and message['text'].startswith("<@%s>" % slack_user_id):

                print ("Message received: %s" % json.dumps(message, indent=2))

                message_text = message['text'].\
                    split("<@%s>" % slack_user_id)[1].\
                    strip()
                    
                if re.match(r'.*(basement).*', message_text, re.IGNORECASE):
                    # uncomment 3 lines below once all arduinos are running
                    tooManyTries = False
                    retry = 0
                    while (retry < 10):
                        try:
                            r = requests.get (url = API_ENDPOINT_BASEMENT, timeout = 10)
                            # extract response text
                            responseText = r.text
                            print("The response was: %s"%responseText)
                            break
                        except:
                            print("Could not get a response from /basement endpoint!")
                            retry += 1
                            if (retry == 10):
                                tooManyTries = True
                    if (tooManyTries == True):
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Could not get a response from /basement endpoint. Please try again later!",
                            as_user=True)
                    else:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=responseText,
                            as_user=True)
                        
                if re.match(r'.*(main).*', message_text, re.IGNORECASE):
                    # uncomment 3 lines below once all arduinos are running
                    tooManyTries = False
                    retry = 0
                    while (retry < 10):
                        try:
                            r = requests.get (url = API_ENDPOINT_MAIN, timeout = 10)
                            # extract response text
                            responseText = r.text
                            print("The response was: %s"%responseText)
                            break
                        except:
                            print("Could not get a response from /main endpoint!")
                            retry += 1
                            if (retry == 10):
                                tooManyTries = True
                    if (tooManyTries == True):
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Could not get a response from /main endpoint. Please try again later!",
                            as_user=True)
                    else:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=responseText,
                            as_user=True)
                if re.match(r'.*(upstairs).*', message_text, re.IGNORECASE):
                    # uncomment 3 lines below once all arduinos are running
                    tooManyTries = False
                    retry = 0
                    while (retry < 10):
                        try:
                            r = requests.get (url = API_ENDPOINT_UPSTAIRS, timeout = 10)
                            # extract response text
                            responseText = r.text
                            print("The response was: %s"%responseText)
                            break
                        except:
                            print("Could not get a response from /upstairs endpoint!")
                            retry += 1
                            if (retry == 10):
                                tooManyTries = True
                    if (tooManyTries == True):
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text="Could not get a response from /upstairs endpoint. Please try again later!",
                            as_user=True)
                    else:
                        slack_client.api_call(
                            "chat.postMessage",
                            channel=message['channel'],
                            text=responseText,
                            as_user=True)
                if re.match(r'.*(fan on).*', message_text, re.IGNORECASE):
                    if FAN_STATE == 'OFF':
                        FAN_STATE = 'ON'
                        print("turn on the fan")
                        call(['./wemo_control2.sh', config.slack['wemo_device_ip'], 'on'])
                        slack_client.api_call(
                                "chat.postMessage",
                                channel=message['channel'],
                                text="Successfully Turned On the fan!",
                                as_user=True)
                if re.match(r'.*(fan off).*', message_text, re.IGNORECASE):
                    if FAN_STATE == 'ON':
                        FAN_STATE = 'OFF'
                        print("turn off the fan")
                        call(['./wemo_control2.sh', config.slack['wemo_device_ip'], 'off'])
                        slack_client.api_call(
                                "chat.postMessage",
                                channel=message['channel'],
                                text="Successfully Turned Off the fan!",
                                as_user=True)
                            
        time.sleep(1)
        