# if pressed the door is opened
# else closed
import threading
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import time
from door_sensor.sensor import button_pressed
from door_sensor.simulation import run_simulation
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass

ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()


def publisher_task(event, ds_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_ds_batch = ds_batch.copy()
            publish_data_counter = 0
            ds_batch.clear()
        publish.multiple(local_ds_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published {publish_data_limit} {settings["name"]} values')
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, ds_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def ds_callback(is_lock, publish_event, ds_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print("DHT1")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"isOpen: {is_lock}%")

    payload = {
        "measurement": ds_settings['topic'],
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "name": ds_settings["name"],
        "value": is_lock
    }

    with counter_lock:
        ds_batch.append((ds_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ds(settings):
    try :
        if settings["simulated"]:
            run_simulation(ds_callback, publish_event, settings)
        else:
            try:
                print("Press x to unlock the door\nPress y to lock the door\n")

                PORT_BUTTON = settings["pin"]
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.add_event_detect(PORT_BUTTON, GPIO.BOTH, callback=button_pressed, bouncetime=100)
                # TODO: 
                input("Press any key to exit...")
            except KeyboardInterrupt:
                print('Simulation stopped by user')
                # GPIO.cleanup()
            except Exception as e:
                print(f'Error: {str(e)}')
                # GPIO.cleanup()
    except KeyboardInterrupt:
        print("DS stopped")


