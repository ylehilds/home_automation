import re
import time
import json
import psutil
import requests
from subprocess import call
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.request import SocketModeRequest
from slack_sdk.socket_mode.response import SocketModeResponse
from subprocess import run, PIPE

# Load config
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import config

# Slack clients
SLACK_BOT_TOKEN = config.slack['slack_client']
SLACK_APP_TOKEN = config.slack['slack_app_token']
slack_client = WebClient(token=SLACK_BOT_TOKEN)
socket_client = SocketModeClient(app_token=SLACK_APP_TOKEN, web_client=slack_client)

# API Endpoints
API_ENDPOINT_BASEMENT = config.aws['sensors_server_ip_address'] + "/temperature/basement"
API_ENDPOINT_MAIN = config.aws['sensors_server_ip_address'] + "/temperature/main"
API_ENDPOINT_UPSTAIRS = config.aws['sensors_server_ip_address'] + "/temperature/upstairs"
FAN_STATE = 'OFF'

# Handle events
def process(client: SocketModeClient, req: SocketModeRequest):
    global FAN_STATE

    if req.type == "events_api":
        event = req.payload.get("event", {})
        client.send_socket_mode_response(SocketModeResponse(envelope_id=req.envelope_id))

        if event.get("type") == "app_mention":
            user = event.get("user")
            channel = event.get("channel")
            text = event.get("text", "")
            message_text = re.sub(r"<@[^>]+>\s*", "", text).strip()

            print(f"Message received from {user}: {message_text}")

            if re.match(r'.*(basement).*', message_text, re.IGNORECASE):
                send_temperature(channel, API_ENDPOINT_BASEMENT, "basement")

            elif re.match(r'.*(main).*', message_text, re.IGNORECASE):
                send_temperature(channel, API_ENDPOINT_MAIN, "main")

            elif re.match(r'.*(upstairs).*', message_text, re.IGNORECASE):
                send_temperature(channel, API_ENDPOINT_UPSTAIRS, "upstairs")

            elif re.match(r'.*(fan on).*', message_text, re.IGNORECASE):
                if FAN_STATE == 'OFF':
                    FAN_STATE = 'ON'
                    print("Turning on the fan")
                    try:
                        result = run(['./wemo_control2.sh', config.slack['wemo_device_ip'], 'on'], stdout=PIPE, stderr=PIPE, text=True, check=True)
                        print("Exit Code:", result.returncode)
                        print("STDOUT:", result.stdout)
                        print("STDERR:", result.stderr)
                    except Exception as e:
                        print("Error running wemo_control2.sh:", str(e))
                    slack_client.chat_postMessage(channel=channel, text="Successfully Turned On the fan!")

            elif re.match(r'.*(fan off).*', message_text, re.IGNORECASE):
                if FAN_STATE == 'ON':
                    FAN_STATE = 'OFF'
                    print("Turning off the fan")
                    try:
                        result = run(['./wemo_control2.sh', config.slack['wemo_device_ip'], 'off'], stdout=PIPE, stderr=PIPE, text=True, check=True) 
                        print("Exit Code:", result.returncode)
                        print("STDOUT:", result.stdout)
                        print("STDERR:", result.stderr)
                    except Exception as e:
                        print("Error running wemo_control2.sh:", str(e))
                    slack_client.chat_postMessage(channel=channel, text="Successfully Turned Off the fan!")

def send_temperature(channel, endpoint, label):
    retry = 0
    tooManyTries = False
    while retry < 10:
        try:
            r = requests.get(url=endpoint, timeout=10)
            response_text = r.text
            print(f"The response from {label} was: {response_text}")
            slack_client.chat_postMessage(channel=channel, text=response_text)
            return
        except Exception as e:
            print(f"Could not get a response from {label} endpoint: {e}")
            retry += 1
            time.sleep(1)

    slack_client.chat_postMessage(
        channel=channel,
        text=f"Could not get a response from /{label} endpoint. Please try again later!"
    )

# Start the socket client
if __name__ == "__main__":
    socket_client.socket_mode_request_listeners.append(process)
    socket_client.connect()
    print("Socket Mode client connected and listening...")
    while True:
        time.sleep(1)
