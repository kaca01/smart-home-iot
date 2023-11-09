import threading
from settings.settings import load_settings
from room_dht.dht1 import run_dht1
from room_dht.dht2 import run_dht2
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
    
    try:
        dht1_settings = settings['DHT1']
        run_dht1(dht1_settings, threads, stop_event_dht1)

        time.sleep(1)
  
        dht2_settings = settings['DHT2']
        run_dht2(dht2_settings, threads, stop_event_dht2)
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for stop_event in [stop_event_dht1, stop_event_dht2]:
            stop_event.set()

        for t in threads:
            t.join()
