#!/bin/sh

if pidof -x "pibotproject.py" > /dev/null; then
    echo "Process already running"
else
    python /home/lehi/dev/home_automation/temperature_sensors/deviceSDK/pibotproject.py >> /dev/null &
    echo "New Instance"
fi
