from dhts.simulator import run_dht_simulator
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading
import time


dht_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, dht_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_dht_batch = dht_batch.copy()
            publish_data_counter = 0
            dht_batch.clear()
        publish.multiple(local_dht_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published {publish_data_limit} {settings["name"]} values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, dht_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def dht_callback(humidity, temperature, publish_event, dht_settings, code="DHTLIB_OK", verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print("DHT1")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Code: {code}")
        print(f"Humidity: {humidity}%")
        print(f"Temperature: {temperature}°C")

    temp_payload = {
        "measurement": dht_settings['topic'][0],
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": temperature
    }

    humidity_payload = {
        "measurement": dht_settings['topic'][1],
        "simulated": dht_settings['simulated'],
        "runs_on": dht_settings["runs_on"],
        "name": dht_settings["name"],
        "value": humidity
    }

    with counter_lock:
        dht_batch.append((dht_settings['topic'][0], json.dumps(temp_payload), 0, True))
        dht_batch.append((dht_settings['topic'][1], json.dumps(humidity_payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, stop_event):
    if settings['simulated']:
        run_dht_simulator(2, dht_callback, stop_event, publish_event, settings)

    else:
        from dhts.sensors import run_dht_loop, DHT
        dht = DHT(settings['pin'])
        run_dht_loop(dht, 2, dht_callback, stop_event, publish_event, settings)
