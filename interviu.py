import paho.mqtt.publish as mqtt
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import json
import time

logfile = "/home/pi/Desktop/Noaje-Alexandra/data.txt"

qos = 0
mHost = "mqtt.beia-telemetrie.ro"
mTopic = "/training/device/alexandra-noaje"
mUser = ""
mPassword = ""

#channel - port used by sensor
channel = 21

#function used to store data in a simple textfile
#it is called each time the sensor detects something
def local_save(data):
    file = open(logfile, "w")
    file.write(data)
    file.close()


def on_connect(client, userdata, flags, rc):
    if(rc==0):
        print("Connected to broker")
        global Connected
    else:
        print("Connected failed")
Connected = False

mqttc = mqtt.Client()
#mqttc.connect(mHost, port=1833, keepalive=60, bind_address="")

mqttc.username_pw_set(mUser, mPassword)
mqttc.on_connect = on_connect
mqttc.connect(mHost, port = 1883)
mqttc.loop_start()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(channel, GPIO.IN)
GPIO.add_event_detect(channel, GPIO.BOTH)


#def on_connect():
#    print("Connected with result code " + str(rc))
#    client.subscribe(mTopic+"/#")
    
#def on_detect_sensor(fTopic, fQos, fHost, fClient, fPayload):
#    fClient.single(fTopic, fQos, fHost, fPayload)

def on_detect_sensor(fTopic, fPayload):
    fClient.publish(fTopic, fPayload)
    
while True:
    if GPIO.event_detected(channel):
        payload = {"SENSOR" : value}
        basic_string = "valoare"
        save_local(basic_string)
        
        on_detect_sensor(mTopic, payload)
        #on_detect_sensor(mTopic, qos, mHost, payload)
        
        time.sleep(15) #wait 15s

    else:
        print("Nothing has been detected so far...")
