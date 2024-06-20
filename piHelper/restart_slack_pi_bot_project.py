#!/bin/sh

if ps -ef | grep -v grep | grep pibotproject ; then
    echo "Running"
else
    /home/lehi/dev/home_automation/temperature_sensors/slack/bin/python /home/lehi/dev/home_automation/temperature_sensors/pibotproject.py
fi
