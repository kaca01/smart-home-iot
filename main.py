import threading
from settings.settings import load_settings
from dhts.dht1 import run_dht1
from dhts.dht2 import run_dht2
from pirs.rpir2 import run_pir2
from buzzer.buzzer import run_buzzer
from door_membrane_switch.door_membrane_switch import run_dms
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    
    stop_event_dht1 = threading.Event()
    stop_event_dht2 = threading.Event()
    stop_event_pir1 = threading.Event()
    stop_event_pir2 = threading.Event()
    
    try:
        # dht1_settings = settings['DHT1']
        # run_dht1(dht1_settings, threads, stop_event_dht1)

        # time.sleep(1)
  
        # dht2_settings = settings['DHT2']
        # run_dht2(dht2_settings, threads, stop_event_dht2)

        # pir2_settings = settings['PIR2']
        # run_pir2(pir2_settings, threads, stop_event_pir2)

        # run_buzzer(settings['DB'])

        run_dms(settings['DMS'])
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Simulation stopped by user")
        for stop_event in [stop_event_dht1, stop_event_dht2, stop_event_pir1, stop_event_pir2]:
            stop_event.set()

        for t in threads:
            t.join()
