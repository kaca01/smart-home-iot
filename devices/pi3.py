import threading
from settings.settings import load_settings
from settings.broker_settings import HOSTNAME, PORT
from dhts.dht import run_dht
from pirs.pir import run_pir
from buzzer.buzzer import run_buzzer
from lights.rgb.rgb_led import run_rgb
from segment_display.segment_display import run_4d7sd
from infrared.infrared import run_infrared
import time
import json
import paho.mqtt.client as mqtt

try:
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
        pass

def print_exit():
        print("""
                        ***   ***
                       ***** *****
                        *********
                         ******* 
                          *****
                           ***
                            *
                """)
        print("Bye!")

def on_message(client, userdata, msg):
        settings = load_settings()
        try:
                payload = json.loads(msg.payload.decode('utf-8'))
                value = payload.get("value")
                if value is not None:
                        run_rgb({"button": value}, settings["RGB"])

        except json.JSONDecodeError as e:
                print(f"JSON error: {e}")
        except Exception as e:
                print(f"Exception: {e}")


def congif_mqtt():
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.connect(HOSTNAME, 1883, 60)
        mqtt_client.subscribe("BIR")
        mqtt_client.loop_start()


if __name__ == "__main__":
        print('START PI3')
        congif_mqtt()
        settings = load_settings()
        threads = []

        # events
        stop_event_pir4 = threading.Event()
        stop_event_dht4 = threading.Event()
        stop_event_bb = threading.Event()
        stop_event_b4sd = threading.Event()
        stop_event_bir = threading.Event()
        stop_event_rgb = threading.Event()

        events = []
        events += [stop_event_pir4, stop_event_dht4, stop_event_bb, stop_event_b4sd, stop_event_bir, stop_event_rgb]

        try:
                # PI3
                thread = threading.Thread(target=run_pir, args=(settings["PIR4"], stop_event_pir4, settings))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT4"], stop_event_dht4))
                thread.start()

                # thread = threading.Thread(target=run_buzzer, args=(settings["BB"], stop_event_bb,))
                # thread.start()
                # threads.append(thread)

                thread = threading.Thread(target=run_4d7sd, args=(settings["B4SD"], stop_event_b4sd,))
                thread.start()
                threads.append(thread)

                thread = threading.Thread(target=run_infrared, args=(settings["BIR"], stop_event_bir,))
                thread.start()

                # thread = threading.Thread(target=run_rgb, args=(settings["RGB"], stop_event_rgb))
                # thread.start()

                while True:
                        time.sleep(1)
        except KeyboardInterrupt:

                for stop_event in events:
                        stop_event.set()

                for t in threads:
                        t.join()

                print("App stopped by user")
                print_exit()
