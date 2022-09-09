#!/bin/sh
# auto.sh

sleep 100
while true
do
  cd /
  cd home/pi/Desktop
  sudo python auto.py
  sleep 30
  cd /
done
