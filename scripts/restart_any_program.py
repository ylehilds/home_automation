#!/bin/sh

if ps -ef | grep -v grep | grep <running_program> ; then
    echo "Running"
else
    python <path_of_program_executable>
fi

# cron job every 5 minutes:
# */5 * * * * sh /home/pi/Desktop/restart_slack_pi_bot_project.sh

# original for example purpose:

#!/bin/sh

#if ps -ef | grep -v grep | grep pibotproject ; then
#    echo "Running"
#else
#    python /home/pi/Documents/deviceSDK/pibotproject.py
#fi
