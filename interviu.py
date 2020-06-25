import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import time

logfile = "/home/pi/Desktop/Noaje-Alexandra/data.txt"

qos = 0
mHost = "mqtt.beia-telemetrie.ro"
mTopic = "/training/rpi/alexandra-noaje"
mUser = ""
mPassword = ""

#channel - port used by sensor
channel = 15

def local_save(data):
    file = open(logfile, "w")
    file.write(data)
    file.close()

def on_connect(client, userdata, flags, rc):
    if(rc==0):
        print("Connected OK.")
    else:
        print("Bad connection.")

mqttc = mqtt.Client()

mqttc.username_pw_set(mUser, mPassword)
mqttc.on_connect = on_connect
mqttc.connect(mHost, port = 1883)
mqttc.loop_start()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH)


def on_detect_sensor(fTopic, fPayload):
    fClient.publish(fTopic, fPayload)
    
while True:
    if GPIO.event_detected(channel):
        payload = {"SENSOR" : value}
        basic_string = "valoare"
        save_local(basic_string)
        
        on_detect_sensor(mTopic, payload)
        time.sleep(1) 

    else:
        print("Nothing has been detected so far...")
