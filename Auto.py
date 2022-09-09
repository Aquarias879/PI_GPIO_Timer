#!/usr/bin/python3
# auto.sh
from influxdb import DataFrameClient
import pandas as pd
import time
import RPi.GPIO as GPIO

fog = 15
fan = 14
heater = 25
water = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(fog, GPIO.OUT)
GPIO.setup(fan, GPIO.OUT)
GPIO.setup(heater, GPIO.OUT)
GPIO.setup(water, GPIO.OUT)

GPIO.output(fog, GPIO.LOW)
GPIO.output(fan, GPIO.LOW)
GPIO.output(heater, GPIO.LOW)
GPIO.output(water, GPIO.LOW)

user = 'sam'
password = '12345678'
dbname = 'Predicted'
host = '203.64.131.98'
port = 8086

client = DataFrameClient(host, port, user, password,dbname)

while True:
    temp1 = client.query('SELECT last("value") FROM "temp_pred" WHERE time > now() - 30s limit 1;')
    humid1 = client.query('SELECT last("value") FROM "hum_pred" WHERE time > now() - 30s limit 1;')
    soil1 = client.query('SELECT last("value") FROM "soil_pred" WHERE time > now() - 30s limit 1;')
    templ = temp1['temperature']
    humidlist = humid1['humidity']
    soillist = soil1['SoilMoisture']
    temp = templ['last']
    humid = humidlist['last']
    soil = soillist['last']
    tempstr= ''.join(map(str,temp))
    humidstr= ''.join(map(str,humid))
    soilstr=''.join(map(str,soil))
    time.sleep(5)

    if tempstr < '24' and tempstr != '0.0':
        GPIO.output(heater,GPIO.HIGH)
        print ("trun on heater")
        if humidstr < '85':
            #GPIO.output(fog,GPIO.HIGH)
            print ("trun on mist")
        elif humidstr > '95':
            GPIO.output(fan,GPIO.HIGH)
            print ("trun on fan")
            time.sleep(20)
            GPIO.output(fan,GPIO.LOW)
            print ("trun off fan")
    elif tempstr > '26' and tempstr != '0.0':
        GPIO.output(heater, GPIO.LOW)
        print ("trun off heater")
        GPIO.output(fan,GPIO.HIGH)
        print ("trun on fan")
        if humidstr < '59':
            #GPIO.output(fog,GPIO.HIGH)
            print ("trun on mist")
        elif humidstr > '65':
            GPIO.output(fan,GPIO.HIGH)
            print ("trun on fan")
            time.sleep(20)
            GPIO.output(fan,GPIO.LOW)
            print ("trun off fan")
    elif humidstr < '85':
        GPIO.output(fan,GPIO.LOW)
        print ("trun on fan")
        if tempstr > '26':
            GPIO.output(heater, GPIO.LOW)
            print ("trun off heater")
        elif tempstr < '24':
            GPIO.output(heater,GPIO.HIGH)
            print ("trun on heater")
    elif humidstr > '95':
        #GPIO.output(fog,GPIO.HIGH)
        GPIO.output(fan,GPIO.HIGH)
        print ("trun on fan")
        time.sleep(20)
        GPIO.output(fan,GPIO.LOW)
        print ("trun off fan")
        if tempstr > '26':
            GPIO.output(heater,GPIO.LOW)
            print ("trun off heater")
            GPIO.output(fan,GPIO.HIGH)
            time.sleep(20)
            GPIO.output(fan,GPIO.LOW)
            print ("trun off fan")
        elif tempstr < '24':
            GPIO.output(heater,GPIO.HIGH)
            print ("trun on heater")
    elif '24' < tempstr < '26':
        if '59' < humidstr < '95':
            #GPIO.output(fog, GPIO.LOW)
            GPIO.output(fan, GPIO.LOW)
            GPIO.output(heater, GPIO.LOW)
            GPIO.output(water, GPIO.LOW)
            print ("climate is stable")
    elif tempstr == '0.0' or humidstr == '0.0':
            #GPIO.output(fog, GPIO.LOW)
            GPIO.output(fan, GPIO.LOW)
            GPIO.output(heater, GPIO.LOW)
            GPIO.output(water, GPIO.LOW)
            print ("error")
    time.sleep(10)
    print (tempstr)
    print (humidstr)
    print (soilstr)
