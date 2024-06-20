#!/bin/sh

if ps -ef | grep -v grep | grep pibotproject.py > /dev/null; then
    echo "Already Running"
else
    /home/lehi/dev/home_automation/temperature_sensors/slack/bin/python /home/lehi/dev/home_automation/temperature_sensors/pibotproject.py >> /dev/null &
    echo "New Instance"
fi
