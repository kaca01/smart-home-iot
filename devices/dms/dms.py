from  dms.simulator import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading
import time
import requests


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


def send_values_to_back(pin):
    try:
        response = requests.post(f'http://{HOSTNAME}:5000/api/dms/send-pin', json={'pin': pin})
        response_data = response.json()

        if response_data['success']:
            print('PIN is send.')
        else:
            print(f'Error: {response_data["error"]}')

    except Exception as e:
        print(f'Error: {str(e)}')


def dms_callback(pin, publish_event, dms_settings, verbose=False):
    global older_value

    send_values_to_back(pin)

    if verbose:
        t = time.localtime()
        print("="*20)
        print("Correct pin")

    dms_payload = {
        "measurement": dms_settings['name'],
        "simulated": dms_settings['simulated'],
        "runs_on": dms_settings["runs_on"],
        "name": "pin",
        "value": pin
    }

    with counter_lock:
        dms_batch.append(('DMS', json.dumps(dms_payload), 0, True))

    if older_value != pin:
        publish_event.set()

    older_value = pin


def run_dms(settings, stop_event):
    try: 
        # if settings['simulated']:
        #     print("DMS sumilator")
        #     run_simulation(EXPECTED_PIN, 2, dms_callback, stop_event, publish_event, settings)
        if not settings['simulated']:
            from dms.sensor import run_sensor
            print("DMS running")
            run_sensor(settings['pin'], 2, dms_callback, stop_event, publish_event, settings)   
    except KeyboardInterrupt:
        print("DMS thread stopped by user")  