# if pressed the door is opened
# else closed
import threading
from settings.broker_settings import HOSTNAME, PORT
import paho.mqtt.publish as publish
import json
import time
from datetime import datetime, timedelta
from door_sensor.sensor import button_pressed
from door_sensor.simulation import run_simulation
from buzzer.buzzer import button_pressed, button_released
from alarm.alarm import turn_on_alarm, turn_off_alarm
import requests


try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass


def is_active_sys():
    url = f"http://{HOSTNAME}:5000/system"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data["data"]
    else:
        return None
    

def get_pin(url):
    response = requests.get(url)

    if response.status_code == 200:
        json_data = response.json()
        return json_data["data"]
    else:
        return None
    
def turn_off_sys():
    url = f"http://{HOSTNAME}:5000/set-sys-activity"
    requests.put(url)

ds_batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
start_time = None


def alarm_activation(event):
    temp_payload = {
                    "measurement": 'ALARM',
                    "simulated": False,
                    "runs_on": 'PI1',
                    "name": "alarm",
                    "value": True
                    }
    start_time = 0
    # buzzer_event = threading.Event()
    while True:
        event.wait()
        print("ALARM")
        start_time = datetime.now()
        event.clear()
        while not event.is_set():
            if (datetime.now() - start_time).total_seconds() > 5:
                print("ALARM JE POCEO")
                turn_on_alarm()
                # button_pressed(buzzer_event)
                # temp_payload["value"] = True
                # with counter_lock:
                #     b = [('ALARM', json.dumps(temp_payload), 0, True)]
                #     publish.multiple(b, hostname=HOSTNAME, port=PORT)
                break
                # event.set()
            
        event.clear()
        event.wait()
        print("ALARM JE ZAVRSIO")
        turn_off_alarm()
        # button_released(buzzer_event)
        # temp_payload["value"] = False
        # with counter_lock:
        #             b = [('ALARM', json.dumps(temp_payload), 0, True)]
        #             publish.multiple(b, hostname=HOSTNAME, port=PORT)
        event.clear()


alarm_event = threading.Event()
alarm_thread = threading.Thread(target=alarm_activation, args=(alarm_event, ))
alarm_thread.daemon = True


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
    global publish_data_counter, publish_data_limit, start_time, alarm_event
    is_open = not is_lock
    alarm_event.set()

    if is_active_sys():
        turn_on_alarm()
    
    if verbose:
        t = time.localtime()
        print("="*20)
        print("DHT1")
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"isOpen: {is_open}")

    payload = {
        "measurement": ds_settings['name'],
        "simulated": ds_settings['simulated'],
        "runs_on": ds_settings["runs_on"],
        "name": "pressed",
        "value": is_lock
    }

    with counter_lock:
        ds_batch.append((ds_settings['topic'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

    if is_open and (start_time is None):
        start_time = datetime.now()
    elif not is_open and (start_time is not None):
        end_time = datetime.now()
        difference = (end_time - start_time).total_seconds()
        start_time = None
        print("DIFFERENCE: ", difference)
        # alarm_event.set()


def run_ds(settings, stop_event):
    global alarm_thread
    alarm_thread.start()
    # alarm_pin_thread.start()
    try :
        if settings["simulated"]:
            print("uslooooooooo")
            run_simulation(ds_callback, publish_event, settings, stop_event)
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
