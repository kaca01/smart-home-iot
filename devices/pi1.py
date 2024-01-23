import threading
from settings.settings import load_settings
from dhts.dht import run_dht
from pirs.pir import run_pir
from buzzer.buzzer import run_buzzer
from dms.dms import run_dms
from door_sensor.door_sensor import run_ds
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus
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
        print('START PI1')
        settings = load_settings()
        threads = []

        # events
        stop_event_dus1 = threading.Event()
        stop_event_db = threading.Event()
        stop_event_dpir1 = threading.Event()
        stop_event_dms = threading.Event()
        stop_event_pir1 = threading.Event()
        stop_event_pir2 = threading.Event()
        stop_event_dht1 = threading.Event()
        stop_event_dht2 = threading.Event()

        events = []
        events += [stop_event_dus1, stop_event_db, stop_event_dpir1, stop_event_dms, stop_event_pir1, stop_event_pir2, stop_event_dht1, stop_event_dht2]

        try:
                # PI1
                thread = threading.Thread(target=run_ds, args=(settings["DS1"],))
                thread.start()

                thread = threading.Thread(target=run_dus, args=(settings["DUS1"], stop_event_dus1,))
                thread.start()

                # thread = threading.Thread(target=run_buzzer, args=(settings["DB"], stop_event_db,))
                # thread.start()
                # threads.append(thread)

                thread = threading.Thread(target=run_pir, args=(settings["DPIR1"], stop_event_dpir1))
                thread.start()

                thread = threading.Thread(target=run_dms, args=(settings["DMS"], stop_event_dms,))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR1"], stop_event_pir1,))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR2"], stop_event_pir2,))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT1"], stop_event_dht1))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT2"], stop_event_dht2))
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
