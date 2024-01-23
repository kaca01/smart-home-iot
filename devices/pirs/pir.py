from pirs.simulator import motion_detection_simulation
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import threading
from lights.door_light import run_dl
import requests

def is_enter():
    url = "http://127.0.0.1:5000/dus1/3"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        # print(json_data["data"])
        data = json_data["data"]
        if data != []:
            if data[0]["_value"] > data[-1]["_value"]:
                return True
            else:
                return False
        else:
            return None
    else:
        return None


pir_batch = []
counter_lock = threading.Lock()


def publisher_task(event, pir_batch):
    while True:
        event.wait()
        with counter_lock:
            local_pir_batch = pir_batch.copy()
            pir_batch.clear()
        publish.multiple(local_pir_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published pir1 values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, pir_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def pir_callback(result, publish_event, pir_settings, settings, rgb_thread, verbose=False):
    if verbose:
        print(f"{pir_settings['name']} says: you moved!")

    temp_payload = {
        "measurement": pir_settings['topic'],
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "name": pir_settings["name"],
        "value": result
    }

    with counter_lock:
        pir_batch.append((pir_settings['topic'], json.dumps(temp_payload), 0, True))

    publish_event.set()

    if (pir_settings["name"] == "PIR1") and result and (not rgb_thread.is_alive()):
        check_is_enter = is_enter()
        if check_is_enter is True:
            url = "http://127.0.0.1:5000/increase-counter"
            requests.put(url)
        elif check_is_enter is not False:
            url = "http://127.0.0.1:5000/decrease-counter"
            requests.put(url)
        try:
            rgb_thread.start()
        except RuntimeError:
            print("error catched")
            rgb_thread.join()
            # rgb_event.clear()  # Clear the event
            # # Now create and start a new thread
            rgb_event = threading.Event()
            rgb_thread = threading.Thread(target=run_dl, args=(settings["DL"], rgb_event))
            rgb_thread.start()
            return rgb_thread
            

def run_pir(pir_settings, stop_event, settings):
    print("Starting pir")

    rgb_event = threading.Event()
    rgb_thread = threading.Thread(target=run_dl, args = (settings["DL"], rgb_event))
    try:
        if pir_settings['simulated']:
            motion_detection_simulation(pir_callback, stop_event, publish_event, pir_settings, settings, rgb_thread)
        else:
            # TODO: add return value for lamp
            from pirs.sensors import run_pir_loop
            run_pir_loop(2, pir_callback, stop_event, publish_event, pir_settings)
    except KeyboardInterrupt:
        print("PIR thread stopped by user")
        stop_event.set()
        rgb_event.set()
