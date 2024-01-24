import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from buzzer.buzzer import button_pressed, button_released
import threading


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


def turn_off_alarm():
    global is_alarm_on
    with lock_alarm:
        button_released(stop_event)
        is_alarm_on = False
        
    
is_alarm_on = False
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = lambda client, userdata, msg: turn_off_alarm()
stop_event = threading.Event()
lock_alarm = threading.Lock()