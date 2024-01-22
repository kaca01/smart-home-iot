import threading
from settings.settings import load_settings
from dhts.dht import run_dht
from pirs.pir import run_pir
from buzzer.buzzer import run_buzzer
from dms.dms import run_dms
from sensors.door_sensor.door_sensor import run_ds1
from lights.door_light import run_dl
from sensors.ultrasonic_sensors.door_ultrasonic_sensor import run_dus1
from pirs.door_motion_sensor import run_dpir1
from lights.rgb.rgb_led import run_rgb
from lcd.lcd import run_lcd
from segment_display.segment_display import run_4d7sd
from infrared.infrared import run_infrared
from gyroscope.gyroscope import run_gyroscope
import time

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

if __name__ == "__main__":
        print('START PI3')
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
                thread = threading.Thread(target=run_pir, args=(settings["PIR4"], stop_event_pir4))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT4"], stop_event_dht4))
                thread.start()

                thread = threading.Thread(target=run_buzzer, args=(settings["BB"], stop_event_bb,))
                thread.start()
                threads.append(thread)

                thread = threading.Thread(target=run_4d7sd, args=(settings["B4SD"], stop_event_b4sd,))
                thread.start()
                threads.append(thread)

                thread = threading.Thread(target=run_infrared, args=(settings["BIR"], stop_event_bir,))
                thread.start()

                thread = threading.Thread(target=run_rgb, args=(settings["RGB"], stop_event_rgb))
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
