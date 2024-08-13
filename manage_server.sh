#!/bin/bash

# Function to start the Flask application
start() {
    nohup flask run > app.log 2>&1 &
    echo "Flask application started"
}

# Function to stop the Flask application
stop() {
    pids=$(ps aux | grep 'flask run' | awk '{print $2}')
    if [ -n "$pids" ]; then
        echo "$pids" | xargs kill
        echo "Flask application stopped"
    else
        echo "Flask application is not running"
    fi
}

# Function to restart the Flask application
restart() {
    stop
    start
}

# Main script
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac
