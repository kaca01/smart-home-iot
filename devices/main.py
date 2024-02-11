import threading
from settings.settings import load_settings
from dhts.dht import run_dht
from pirs.pir import run_pir
from buzzer.buzzer import run_buzzer
from dms.dms import run_dms
from door_sensor.door_sensor import run_ds
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus
from lcd.lcd import run_lcd
from gyroscope.gyroscope import run_gyroscope
from buzzer.buzzer import run_buzzer
from lights.rgb.rgb_led import run_rgb
from segment_display.segment_display import run_4d7sd
from infrared.infrared import run_infrared
import time
import json
import paho.mqtt.client as mqtt


threads = []
events = []

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
            if msg.topic == "BIR":
                run_rgb({"button": value}, settings["RGB"])
            elif msg.topic == "GTEMP":
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
    mqtt_client.connect("localhost", 1883, 60)
    mqtt_client.subscribe("BIR")
    mqtt_client.subscribe("GTEMP")
    mqtt_client.subscribe("GHMD")
    mqtt_client.loop_start()


def config_alarm():
    pass

    # thread = threading.Thread(target=run_pir, args=(settings["DPIR1"], stop_event_dpir1, settings))
    # thread.start()


def run_pi1(settings):
    global events

    stop_event_dus1 = threading.Event()
    stop_event_db = threading.Event()
    stop_event_dpir1 = threading.Event()
    stop_event_dms = threading.Event()
    stop_event_pir1 = threading.Event()
    stop_event_pir2 = threading.Event()
    stop_event_dht1 = threading.Event()
    stop_event_dht2 = threading.Event()

    events += [stop_event_dus1, stop_event_db, stop_event_dpir1, stop_event_dms, stop_event_pir1, stop_event_pir2, stop_event_dht1, stop_event_dht2]

    # PI1
    thread = threading.Thread(target=run_ds, args=(settings["DS1"], ))
    thread.start()

    thread = threading.Thread(target=run_dus, args=(settings["DUS1"], stop_event_dus1,))
    thread.start()

    # thread = threading.Thread(target=run_buzzer, args=(settings["DB"], stop_event_db,))
    # thread.start()
    # threads.append(thread)

    thread = threading.Thread(target=run_pir, args=(settings["DPIR1"], stop_event_dpir1, settings))
    thread.start()

    thread = threading.Thread(target=run_dms, args=(settings["DMS"], stop_event_dms,))
    thread.start()

    thread = threading.Thread(target=run_pir, args=(settings["PIR1"], stop_event_pir1, settings))
    thread.start()

    thread = threading.Thread(target=run_pir, args=(settings["PIR2"], stop_event_pir2, settings))
    thread.start()

    thread = threading.Thread(target=run_dht, args=(settings["DHT1"], stop_event_dht1))
    thread.start()

    thread = threading.Thread(target=run_dht, args=(settings["DHT2"], stop_event_dht2))
    thread.start() 


def run_pi2(settings):
    global events

    stop_event_dus2 = threading.Event()
    stop_event_dpir2 = threading.Event()
    stop_event_gdht = threading.Event()
    stop_event_lcd = threading.Event()
    stop_event_gsg = threading.Event()
    stop_event_pir3 = threading.Event()
    stop_event_dht3 = threading.Event()

    events += [stop_event_dus2, stop_event_dpir2, stop_event_gdht, stop_event_lcd, stop_event_gsg, stop_event_pir3, stop_event_dht3]

    # PI2
    thread = threading.Thread(target=run_ds, args=(settings["DS2"],))
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


def run_pi3(settings):
    global events

    stop_event_pir4 = threading.Event()
    stop_event_dht4 = threading.Event()
    stop_event_bb = threading.Event()
    stop_event_b4sd = threading.Event()
    stop_event_bir = threading.Event()
    stop_event_rgb = threading.Event()

    events += [stop_event_pir4, stop_event_dht4, stop_event_bb, stop_event_b4sd, stop_event_bir, stop_event_rgb]

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


if __name__ == "__main__":
    print('START APP')
    congif_mqtt()
    config_alarm()

    settings = load_settings()

    try:
        run_pi3(settings)
        run_pi2(settings)
        run_pi1(settings)
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        for stop_event in events:
                stop_event.set()

        for t in threads:
                t.join()

        print("App stopped by user")
        print_exit()