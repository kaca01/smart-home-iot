import threading
from settings.settings import load_settings
from dhts.dht import run_dht
from pirs.pir import run_pir
from door_sensor.door_sensor import run_ds
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus
from lcd.lcd import run_lcd
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
        stop_event_dpir2 = threading.Event()
        stop_event_gdht = threading.Event()
        stop_event_lcd = threading.Event()
        stop_event_gsg = threading.Event()
        stop_event_pir3 = threading.Event()
        stop_event_dht3 = threading.Event()

        events = []
        events += [stop_event_dus2, stop_event_dpir2, stop_event_gdht, stop_event_lcd, stop_event_gsg, stop_event_pir3, stop_event_dht3]

        try:
                # PI2
                thread = threading.Thread(target=run_ds, args=(settings["DS2"],))
                thread.start()

                thread = threading.Thread(target=run_dus, args=(settings["DUS2"], stop_event_dus2, ))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["DPIR2"], stop_event_dpir2))
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
