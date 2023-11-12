import threading
from settings.settings import load_settings
from dhts.dht1 import run_dht1
from dhts.dht2 import run_dht2
from pirs.rpir2 import run_pir2
from buzzer.buzzer import run_buzzer
from door_membrane_switch.door_membrane_switch import run_dms
from sensors.door_sensor import run_ds1
from lights.door_light import run_dl
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus1
from pirs.door_motion_sensor import run_dpir1
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
        # door sensor
        # ds1_settings = settings["DS1"]
        # run_ds1(ds1_settings)

        # door light
        # dl_settings = settings["DL"]
        # run_dl(dl_settings)

        # door ultrasonic sensor
        # dus1_settings = settings["DUS1"]
        # run_dus1(dus1_settings)

        # door motion sensor
        dpir1_settings = settings["DPIR1"]
        run_dpir1(dpir1_settings)

        # For DHT uncomment this
        # dht1_settings = settings['DHT1']
        # run_dht1(dht1_settings, threads, stop_event_dht1)

        # time.sleep(1)
  
        # dht2_settings = settings['DHT2']
        # run_dht2(dht2_settings, threads, stop_event_dht2)

        # For PIR uncomment this
        # pir2_settings = settings['PIR2']
        # run_pir2(pir2_settings, threads, stop_event_pir2)

        # For buzzer uncomment this
        # run_buzzer(settings['DB'])

        # For DMS uncomment this
        # run_dms(settings['DMS'])
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("Simulation stopped by user")
        for stop_event in [stop_event_dht1, stop_event_dht2, stop_event_pir1, stop_event_pir2]:
            stop_event.set()

        for t in threads:
            t.join()
