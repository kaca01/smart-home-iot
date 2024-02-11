import time
import random
from time import sleep
from ultrasonic_sensors.simulation import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import threading
import json
import paho.mqtt.publish as publish


dus_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()

def publisher_task(event, dus_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dus_batch = dus_batch.copy()
            publish_data_counter = 0
            dus_batch.clear()
        publish.multiple(local_dus_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published {publish_data_limit} DUS values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dus_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dus_callback(distance, publish_event, dus_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print("DUS")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Distance: {distance}cm")

    payload = {
        "measurement": dus_settings['name'],
        "simulated": dus_settings['simulated'],
        "runs_on": dus_settings["runs_on"],
        "name": "distance",
        "value": distance
    }

    with counter_lock:
        dus_batch.append((dus_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dus(settings, event):
    try:
        if settings["simulated"]:
            run_simulation(event, dus_callback, publish_event, settings)
        else:
            # real-time
            from ultrasonic_sensors.sensor import run_dus_loop
            run_dus_loop(settings, dus_callback, publish_event, event)
    except KeyboardInterrupt:
        print("DUS thread stopped by user")
