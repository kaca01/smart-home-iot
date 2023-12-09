from pirs.simulator import motion_detection_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading


pir_batch = []
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        print(f'published pir1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(result, publish_event, pir_settings, verbose=False):
    if verbose:
        print("PIR1 says: you moved!")

    temp_payload = {
        "measurement": "Motion1",
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "name": pir_settings["name"],
        "value": result
    }

    with counter_lock:
        pir_batch.append(('Motion1', json.dumps(temp_payload), 0, True))

    publish_event.set()


def run_pir1(settings, stop_event):
    if settings['simulated']:
        motion_detection_simulation(pir_callback, stop_event, publish_event, settings)
    else:
        from pirs.sensors import run_pir_loop, PIR
        print("Starting pir1 loop")
        pir = PIR(settings['pin'])
        run_pir_loop(pir, 2, stop_event)
        print("Pir1 loop started")
