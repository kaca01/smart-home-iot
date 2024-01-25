import threading
from settings.settings import load_settings
from settings.broker_settings import HOSTNAME, PORT
from dhts.dht import run_dht
from pirs.pir import run_pir
from door_sensor.door_sensor import run_ds
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus
from lcd.lcd import run_lcd
from gyroscope.gyroscope import run_gyroscope
import time
import json
import paho.mqtt.client as mqtt
from settings.broker_settings import HOSTNAME

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
                if msg.topic == "GTEMP":
                        run_lcd({"temperature": value}, settings["LCD"])
                elif msg.topic == "GHMD":
                        run_lcd({"humidity": value}, settings["LCD"])

    except json.JSONDecodeError as e:
        print(f"JSON error: {e}")
    except Exception as e:
        print(f"Exception: {e}")
    

def congif_mqtt():
        mqtt_client = mqtt.Client()
        mqtt_client.on_message = on_message
        mqtt_client.connect(HOSTNAME, 1883, 60)
        mqtt_client.subscribe("GTEMP")
        mqtt_client.subscribe("GHMD")
        mqtt_client.loop_start()


if __name__ == "__main__":
        print('START PI2')
        congif_mqtt()
        settings = load_settings()
        threads = []

        # events
        stop_event_dus2 = threading.Event()
        stop_event_dpir2 = threading.Event()
        stop_event_gdht = threading.Event()
        stop_event_lcd = threading.Event()
        stop_event_gsg = threading.Event()
        stop_event_pir3 = threading.Event()
        stop_event_dht3 = threading.Event()
        stop_event_ds2 = threading.Event()

        events = []
        events += [stop_event_dus2, stop_event_dpir2, stop_event_gdht, stop_event_lcd, stop_event_gsg, stop_event_pir3, stop_event_dht3, 
                   stop_event_ds2]

        try:
                # PI2
                thread = threading.Thread(target=run_ds, args=(settings["DS2"], stop_event_ds2, ))
                thread.start()

                thread = threading.Thread(target=run_dus, args=(settings["DUS2"], stop_event_dus2, ))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["DPIR2"], stop_event_dpir2, settings))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["GDHT"], stop_event_gdht))
                thread.start()

                # thread = threading.Thread(target=run_lcd, args=(settings["LCD"], stop_event_lcd))
                # thread.start()

                thread = threading.Thread(target=run_gyroscope, args=(settings["GSG"], stop_event_gsg))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR3"], stop_event_pir3, settings))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT3"], stop_event_dht3))
                thread.start()

                while True:
                        time.sleep(1)
        except KeyboardInterrupt:

                for stop_event in events:
                        stop_event.set()

                for t in threads:
                        t.join()

                print("App stopped by user")
                print_exit()
