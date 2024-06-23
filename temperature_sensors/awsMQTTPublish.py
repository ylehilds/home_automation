#!/usr/bin/python

import json
import requests

## Secrets
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config


# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

API_ENDPOINT_BASEMENT = config.aws['sensors_server_ip_address'] + "/temperature/basement"
API_ENDPOINT_MAIN = config.aws['sensors_server_ip_address'] + "/temperature/main"
API_ENDPOINT_UPSTAIRS = config.aws['sensors_server_ip_address'] + "/temperature/upstairs"

# For certificate based connection
myMQTTClient = AWSIoTMQTTClient(config.aws['aws_iot_mqtt_client'])
# For Websocket connection
# myMQTTClient = AWSIoTMQTTClient("myClientID", useWebsocket=True)
# Configurations
# For TLS mutual authentication
myMQTTClient.configureEndpoint(config.aws['aws_iot_mqtt_client_end_point'], config.aws['aws_iot_mqtt_client_end_point_port'])
# For Websocket
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
# For TLS mutual authentication with TLS ALPN extension
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 443)
myMQTTClient.configureCredentials(config.aws['root_ca_path'] + "/AmazonRootCA1.pem", config.aws['root_ca_path'] + "/bed3f412f9-private.pem.key", config.aws['root_ca_path'] + "/bed3f412f9-certificate.pem.crt")
# For Websocket, we only need to configure the root CA
# myMQTTClient.configureCredentials("YOUR/ROOT/CA/PATH")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec


tooManyTries = False
retry = 0
while (retry < 10):
    
    try:
        r = requests.get (url = API_ENDPOINT_BASEMENT, timeout = 10)
        # extract response text
        responseText = r.text
        print("The response was: %s"%responseText)
        myMQTTClient.connect()
        myMQTTClient.publish("IoTTemperatureProject", responseText, 0)
        break
    except:
        print("Could not get a response from /basement endpoint!")
        retry += 1
        if (retry == 10):
            tooManyTries = True
    if (tooManyTries == True):
        message = {"room": "basement", "temperature": "0"}
        myMQTTClient.publish("IoTTemperatureProject", message, 0)

tooManyTries = False
retry = 0
while (retry < 10):
    try:
        r = requests.get (url = API_ENDPOINT_MAIN, timeout = 10)
        # extract response text
        responseText = r.text
        print("The response was: %s"%responseText)
        myMQTTClient.connect()
        myMQTTClient.publish("IoTTemperatureProject", responseText, 0)
        break
    except:
        print("Could not get a response from /main endpoint!")
        retry += 1
        if (retry == 10):
            tooManyTries = True
    if (tooManyTries == True):
        message = {"room": "main", "temperature": "0"}
        myMQTTClient.publish("IoTTemperatureProject", message, 0)


tooManyTries = False
retry = 0
while (retry < 10):
    try:
        r = requests.get (url = API_ENDPOINT_UPSTAIRS, timeout = 10)
        # extract response text
        responseText = r.text
        print("The response was: %s"%responseText)
        myMQTTClient.connect()
        myMQTTClient.publish("IoTTemperatureProject", responseText, 0)
        break
    except:
        print("Could not get a response from /upstairs endpoint!")
        retry += 1
        if (retry == 10):
            tooManyTries = True
    if (tooManyTries == True):
        message = {"room": "upstairs", "temperature": "0"}
        myMQTTClient.publish("IoTTemperatureProject", message, 0)


'''
# reading 2
r = requests.get (url = API_ENDPOINT_MAIN)
# extract response text
responseText = r.text
print("The response was: %s"%responseText)
message = {"foo": "bar"}
myMQTTClient.connect()
myMQTTClient.publish("IoTTemperatureProject", responseText, 0)

# reading 3
r = requests.get (url = API_ENDPOINT_UPSTAIRS)
# extract response text
responseText = r.text
print("The response was: %s"%responseText)
message = {"foo": "bar"}
myMQTTClient.connect()
myMQTTClient.publish("IoTTemperatureProject", responseText, 0)
'''

# MQTT AWS Disconnect
myMQTTClient.disconnect()