from gyroscope.simulator import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
from alarm.alarm import turn_on_alarm
import json
import threading
import requests
import math


gsg_batch = []
counter_lock = threading.Lock()

def get_displacement():
    global buzzer_event
    url = "http://127.0.0.1:5000/gyro/accel.x/10"
    print("URL ", url)
    response = requests.get(url)
    x_accel_data = response.json()["data"]

    url = "http://127.0.0.1:5000/gyro/accel.y/10"
    y_accel_data = requests.get(url).json()["data"]

    url = "http://127.0.0.1:5000/gyro/accel.z/10"
    z_accel_data = requests.get(url).json()["data"]

    if response.status_code == 200:
        if x_accel_data or y_accel_data or z_accel_data != []: 
            x1 = x_accel_data[0]["_value"]
            x2 = x_accel_data[-1]["_value"]
            y1 = y_accel_data[0]["_value"]
            y2 = y_accel_data[-1]["_value"]
            z1 = z_accel_data[0]["_value"]
            z2 = z_accel_data[-1]["_value"]
            displacement = round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2), 3)
            if displacement > 0.21:
                # TODO: this is alarm and it won't stop until 4. task is implemented
                turn_on_alarm()
                temp_payload = {
                    "measurement": 'ALARM',
                    "simulated": False,
                    "runs_on": 'PI2',
                    "name": "alarm",
                    "value": True
                }

                with counter_lock:
                    b = [('ALARM', json.dumps(temp_payload), 0, True)]
                    publish.multiple(b, hostname=HOSTNAME, port=PORT)


def publisher_task(event, gsg_batch):
    while True:
        event.wait()
        with counter_lock:
            local_gsg_batch = gsg_batch.copy()
            gsg_batch.clear()
        publish.multiple(local_gsg_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, gsg_batch,))
publisher_thread.daemon = True
publisher_thread.start()
buzzer_event = threading.Event()

def gsg_callback(result, publish_event, gsg_settings, verbose=True):
    if verbose:
        print("GSG")

    gsg_payload = {
        "measurement": gsg_settings['name'],
        "simulated": gsg_settings['simulated'],
        "runs_on": gsg_settings["runs_on"],
        "name": "",
        "value": result
    }
    get_displacement()
    with counter_lock:
        gsg_batch.append((gsg_settings['topic'], json.dumps(gsg_payload), 0, True))

    publish_event.set()


def run_gyroscope(settings, stop_event):
    try:
        if settings['simulated']:
            run_simulation(2, gsg_callback, stop_event, publish_event, settings)
        else:
            from infrared.sensor import run_sensor
            run_sensor(2, gsg_callback, stop_event, publish_event, settings)
    except KeyboardInterrupt:
        print("GSG thread stopped by user")

