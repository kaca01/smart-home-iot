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
        print('START PI2')
        settings = load_settings()
        threads = []

        # events
        stop_event_dus2 = threading.Event()
        stop_event_gdht = threading.Event()
        stop_event_lcd = threading.Event()
        stop_event_gsg = threading.Event()
        stop_event_pir3 = threading.Event()
        stop_event_dht3 = threading.Event()

        events = []
        events += [stop_event_dus2, stop_event_gdht, stop_event_lcd, stop_event_gsg, stop_event_pir3, stop_event_dht3]

        try:
                # PI2
                thread = threading.Thread(target=run_ds1, args=(settings["DS2"],))
                thread.start()

                thread = threading.Thread(target=run_dus1, args=(settings["DUS2"], stop_event_dus2, ))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["GDHT"], stop_event_gdht))
                thread.start()

                thread = threading.Thread(target=run_lcd, args=(settings["LCD"], stop_event_lcd))
                thread.start()

                thread = threading.Thread(target=run_gyroscope, args=(settings["GSG"], stop_event_gsg))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR3"], stop_event_pir3))
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
