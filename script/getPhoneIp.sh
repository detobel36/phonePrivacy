#!/bin/bash
CREATE_AP_PATH="./create_ap/create_ap"
VIRTUAL_INTERFACE="wlo1"

# Get the PID of created wifi network
PID=`$CREATE_AP_PATH --list-running | grep $VIRTUAL_INTERFACE | cut -d ' ' -f 1`
# Get the list of client connected to the network (normally only one)
RESULT=`$CREATE_AP_PATH --list-clients $PID | sed -n 2p | tr -s ' ' | cut -d ' ' -f 2`

echo $RESULT