from infrared.simulator import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading


bir_batch = []
counter_lock = threading.Lock()


def publisher_task(event, bir_batch):
    while True:
        event.wait()
        with counter_lock:
            local_bir_batch = bir_batch.copy()
            bir_batch.clear()
        publish.multiple(local_bir_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, bir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def bir_callback(result, publish_event, bir_settings, verbose=False):
    if verbose:
        print("nesto se desilo sa rgb")

    rgb_payload = {
        "measurement": bir_settings['name'],
        "simulated": bir_settings['simulated'],
        "runs_on": bir_settings["runs_on"],
        "name": "pressed button",
        "value": result
    }

    with counter_lock:
        bir_batch.append((bir_settings['topic'], json.dumps(rgb_payload), 0, True))

    publish_event.set()


def run_infrared(settings, stop_event):
    try:
        # simulated is done on server side and front 
        if not settings['simulated']:
            from infrared.sensor import run_sensor
            run_sensor(2, bir_callback, stop_event, publish_event, settings)
    except KeyboardInterrupt:
        print("BIR thread stopped by user")

