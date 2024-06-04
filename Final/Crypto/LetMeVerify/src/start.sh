#!/usr/bin/env sh

echo "Server Started on port 5000"
while true; do
    socat TCP-LISTEN:5000,fork,reuseaddr EXEC:"python3 app.py",stderr
    sleep 0.5
done
