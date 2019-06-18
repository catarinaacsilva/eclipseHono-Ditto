#! /bin/bash
firefox http://192.168.85.204:8080/api/2/things/demo:laptop & 
source ./venv/bin/activate
python3 laptop_sensor.py
