from gyroscope.simulator import run_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading


gsg_batch = []
counter_lock = threading.Lock()


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


def gsg_callback(result, publish_event, gsg_settings, verbose=False):
    if verbose:
        print("GSG")

    gsg_payload = {
        "measurement": gsg_settings['topic'],
        "simulated": gsg_settings['simulated'],
        "runs_on": gsg_settings["runs_on"],
        "name": gsg_settings["name"],
        "value": result
    }

    print(result)

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

