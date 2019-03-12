#!/bin/sh
#launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /home/pi/indCap

if [ ! $(pgrep -f tweetCapture.py) ]; then
	    echo "Not Running So starting"
	    nohup python tweetCapture.py
fi
