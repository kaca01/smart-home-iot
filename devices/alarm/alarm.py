import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from buzzer.buzzer import button_pressed, button_released
from settings.broker_settings import HOSTNAME, PORT
import threading
import json


def on_connect(client, userdata, flags, rc):
    topics = ["TURN_OFF_ALARM"]

    for topic in topics:
        client.subscribe(topic)


def turn_on_alarm():
    global is_alarm_on
    if not is_alarm_on:
        with lock_alarm:
            button_pressed(stop_event)
            is_alarm_on = True
            temp_payload = {
                    "measurement": 'ALARM',
                    "simulated": False,
                    "runs_on": 'PI2',
                    "name": "alarm",
                    "value": True
                }
            b = [('ALARM', json.dumps(temp_payload), 0, True)]
            publish.multiple(b, hostname=HOSTNAME, port=PORT)


def turn_off_alarm():
    global is_alarm_on
    with lock_alarm:
        button_released(stop_event)
        is_alarm_on = False
        temp_payload = {
                    "measurement": 'ALARM',
                    "simulated": False,
                    "runs_on": 'PI2',
                    "name": "alarm",
                    "value": False
                }
        b = [('ALARM', json.dumps(temp_payload), 0, True)]
        publish.multiple(b, hostname=HOSTNAME, port=PORT)
        
    
is_alarm_on = False
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: turn_off_alarm()
stop_event = threading.Event()
lock_alarm = threading.Lock()