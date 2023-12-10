from  dms.simulator import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading
import time


dms_batch = []
counter_lock = threading.Lock()


def publisher_task(event, dms_batch):
    while True:
        event.wait()
        with counter_lock:
            local_dms_batch = dms_batch.copy()
            dms_batch.clear()
        publish.multiple(local_dms_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dms_batch,))
publisher_thread.daemon = True
publisher_thread.start()

older_value = ""


def dms_callback(temperature, publish_event, dms_settings, verbose=False):
    global older_value

    if verbose:
        t = time.localtime()
        print("="*20)
        print("Correct pin")

    temp_payload = {
        "measurement": "DMS",
        "simulated": dms_settings['simulated'],
        "runs_on": dms_settings["runs_on"],
        "name": dms_settings["name"],
        "value": temperature
    }

    with counter_lock:
        dms_batch.append(('DMS', json.dumps(temp_payload), 0, True))

    if older_value != temperature:
        publish_event.set()

    older_value = temperature


EXPECTED_PIN = "1212"

def run_dms(settings, stop_event):
    if settings['simulated']:
        print("DMS sumilator")
        run_simulation(EXPECTED_PIN, 2, dms_callback, stop_event, publish_event, settings)
    else:
        from dms.sensor import run_sensor
        print("DMS running")
        run_sensor(settings['pin'], EXPECTED_PIN, 2, dms_callback, stop_event, publish_event, settings)     