#!/bin/bash
LOGFILE="/home/vikram/Desktop/cronjob.log"


log_message() {
    echo "$(date) - $1" >> $LOGFILE
}


log_message "Starting Xvfb..."
Xvfb :1 -screen 0 1024x768x24 &
export DISPLAY=:1


log_message "Running stocks.py..."
/usr/bin/python3 /home/vikram/Desktop/stocks.py >> $LOGFILE 2>&1


log_message "stocks.py completed."

