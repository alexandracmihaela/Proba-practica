import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import time
from sense_hat import SenseHat

sense = SenseHat()

#logfile = "/home/pi/Desktop/Noaje-Alexandra/data.txt"
logfile = "data.txt"

mHost = "mqtt.beia-telemetrie.ro"
mTopic = "training/rpi/alexandra-noaje"
mUser = ""
mPassword = ""

channel = 15

def local_save(data):
    file = open(logfile, "a+")
    file.write(data + "\r\n")
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

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(channel, GPIO.IN)
#GPIO.add_event_detect(channel, GPIO.BOTH)

 
  
def on_detect_sensor(fTopic, fPayload):
    mqttc.publish(fTopic, json.dumps(fPayload))
    
while True:
    t = sense.get_temperature()
    p = sense.get_pressure()
    h = sense.get_humidity()
    payload = {"Temperatura:" : t,
               "Presiune:": p,
               "Umiditate:": h}
    message = "Temperature: " + str(t) + " Pressure: " + str(p) + " Humidity: " + str(h)
    local_save(message)
    on_detect_sensor(mTopic, payload)
    
    print("temperatura" , round(t,3))
    print("presiune" , round(p,3))
    print("umiditate" , round(h,3))
    
    time.sleep(3)     
