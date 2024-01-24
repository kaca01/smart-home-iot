
from time import sleep
import threading
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
from lights.rgb.simulator import run_simulation
from lights.rgb.sensor import run_rgb as run_sensor
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass


rgb_batch = []
counter_lock = threading.Lock()

def publisher_task(event, rgb_batch):
    while True:
        event.wait()
        with counter_lock:
            local_rgb_batch = rgb_batch.copy()
            rgb_batch.clear()
        publish.multiple(local_rgb_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published rgb values')
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, rgb_batch,))
publisher_thread.daemon = True
publisher_thread.start()

def rgb_callback(result, publish_event, pir_settings, verbose=False):
    if verbose:
        print(f"{pir_settings['name']} says: you moved!")

    print("aaaaaaaa")
    print(result)

    temp_payload = {
        "measurement": pir_settings['name'],
        "simulated": pir_settings['simulated'],
        "runs_on": pir_settings["runs_on"],
        "name": "action",
        "value": result
    }

    with counter_lock:
        rgb_batch.append((pir_settings['topic'], json.dumps(temp_payload), 0, True))
    publish_event.set()


def run_rgb(button, settings):
    try:
        if settings["simulated"]:
            print(button["button"])
            run_simulation(rgb_callback, publish_event, settings, button["button"])
        else:
            run_sensor(rgb_callback, publish_event, settings, button)
    except KeyboardInterrupt or EOFError:
        print("RGB stopped by user")
    except Exception as e:
        print(f'Error in RGB: {str(e)}')
                