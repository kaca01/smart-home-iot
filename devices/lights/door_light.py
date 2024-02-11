from lights.simulator import run_simulation
import threading
import paho.mqtt.publish as publish
from settings.broker_settings import HOSTNAME, PORT
import json
try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass
import time

# kada dpir1 detektuje pokret, lampica treba da svetli 10 sekundi
def switch_light(pin, callback, publish_event, settings):
    GPIO.output(pin, GPIO.HIGH)
    callback(True, publish_event, settings)
    time.sleep(10)
    GPIO.output(pin, GPIO.LOW)
    callback(False, publish_event, settings)

led_callback_batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()


def publisher_task(event, led_callback_batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_led_callback_batch = led_callback_batch.copy()
            publish_data_counter = 0
            led_callback_batch.clear()
        publish.multiple(local_led_callback_batch, hostname=HOSTNAME, port=PORT)
        # print(f'published {publish_data_limit} {settings["name"]} values')

        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, led_callback_batch,))
publisher_thread.daemon = True
publisher_thread.start()


def led_callback(isOn, publish_event, led_settings, verbose=False):
    global publish_data_counter, publish_data_limit

    if verbose:
        t = time.localtime()
        print("="*20)
        print(led_settings)
        print(led_settings["name"])
        print(f"Timestamp: {time.strftime('%H:%M:%S', t)}")
        print(f"Is on: {isOn}")

    temp_payload = {
        "measurement": led_settings["name"],
        "simulated": led_settings['simulated'],
        "runs_on": led_settings["runs_on"],
        "name": "isOn",
        "value": isOn
    }

    with counter_lock:
        led_callback_batch.append((led_settings['topic'], json.dumps(temp_payload), 0, True))
        publish_data_counter += 1

    # if publish_data_counter >= publish_data_limit:
    publish_event.set()


def run_dl(settings, stop_event):
    global publish_event
    pin = settings['pin']

    if settings["simulated"]:
        run_simulation(stop_event, led_callback, publish_event, settings)
    else:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT)

        try:
            while True:
                switch_light(pin, led_callback, publish_event, settings)
        except KeyboardInterrupt:
            print('Simulation stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')
