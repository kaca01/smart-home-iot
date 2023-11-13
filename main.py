import threading
from settings.settings import load_settings
from dhts.dht1 import run_dht1
from dhts.dht2 import run_dht2
from pirs.rpir1 import run_pir1
from pirs.rpir2 import run_pir2
from buzzer.buzzer import run_buzzer
from door_membrane_switch.door_membrane_switch import run_dms
from sensors.door_sensor import run_ds1
from lights.door_light import run_dl
from ultrasonic_sensors.door_ultrasonic_sensor import run_dus1
from pirs.door_motion_sensor import run_dpir1
from menu_prints import print_lights_menu, print_main_menu, print_door_sensors_menu, print_exit, print_room_sensors_menu
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass


def handle_lights_menu():
    while True:
        print_lights_menu()
        inp = str(input(""))
        inp = inp.strip().lower()
        if inp == "0":
            break
        elif inp == "1":
            dl_settings = settings["DL"]
            run_dl(dl_settings, '1')
        elif inp == "2":
            dl_settings = settings["DL"]
            run_dl(dl_settings, '2')
        else:
            print("Invalid input!")
    main()


def handle_door_sensors_menu():
    while True:
        print_door_sensors_menu()
        inp = str(input(""))
        inp = inp.strip().lower()
        if inp == "0":
            break
        elif inp == "1":
            dus1_settings = settings["DUS1"]
            thread = threading.Thread(target=run_dus1, args=(dus1_settings, stop_event_dus1))
            thread.start()
        elif inp == "2":
            stop_event_dus1.set()
        elif inp == "3":
            dpir1_settings = settings["DPIR1"]
            thread = threading.Thread(target=run_dpir1, args=(dpir1_settings, stop_event_dpir1))
            thread.start()
        elif inp == "4":
            stop_event_dpir1.set()
        else:
            print("Invalid input!")
    main()


def handle_room_sensors_menu():
    while True:
        print_room_sensors_menu()
        inp = str(input(""))
        inp = inp.strip().lower()
        if inp == "0":
            break
        elif inp == "1":
            thread = threading.Thread(target=run_pir1, args=(settings["PIR1"], threads, stop_event_pir1,))
            thread.start()
        elif inp == "2":
            stop_event_pir1.set()
        elif inp == "3":
            thread = threading.Thread(target=run_pir2, args=(settings["PIR2"], threads, stop_event_pir2,))
            thread.start()
        elif inp == "4":
            stop_event_pir2.set()
        elif inp == "5":
            stop_event_dht1.clear()
            thread = threading.Thread(target=run_dht1, args=(settings["DHT1"], threads, stop_event_dht1))
            thread.start()
        elif inp == "6":
            stop_event_dht1.set()
        elif inp == "7":
            stop_event_dht2.clear()
            thread = threading.Thread(target=run_dht2, args=(settings["DHT2"], threads, stop_event_dht2))
            thread.start()
        elif inp == "8":
            stop_event_dht2.set()
        else:
            print("Invalid input!")

    main()


def main():
    while True:
        print_main_menu()
        inp = str(input(""))
        inp = inp.strip().lower()
        if inp == "0":
            for event in events:
                event.set()
            print_exit()
            exit()
        elif inp == "1":
            ds1_settings = settings["DS1"]
            run_ds1(ds1_settings)
        elif inp == "2":
            handle_lights_menu()
        elif inp == "3":
            handle_door_sensors_menu()
        elif inp == "4":
            run_buzzer(settings['DB'])
        elif inp == "5":
            handle_room_sensors_menu()
        elif inp == "6":
            run_dms(settings["DMS"])
        else:
            print("Invalid input!")


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []

    # events
    stop_event_dht1 = threading.Event()
    stop_event_dht2 = threading.Event()
    stop_event_pir1 = threading.Event()
    stop_event_pir2 = threading.Event()
    stop_event_ds1 = threading.Event()
    stop_event_dl = threading.Event()
    stop_event_dus1 = threading.Event()
    stop_event_dpir1 = threading.Event()

    events = []
    events += [stop_event_dht1, stop_event_dht2, stop_event_pir1, stop_event_pir2, stop_event_ds1, stop_event_dl,
               stop_event_dus1, stop_event_dpir1]

    try:
        main()
    except KeyboardInterrupt:
        print("App stopped by user")
        for stop_event in [stop_event_dht1, stop_event_dht2, stop_event_pir1, stop_event_pir2, stop_event_ds1,
                           stop_event_dl, stop_event_dus1, stop_event_dpir1]:
            stop_event.set()

        for t in threads:
            t.join()
        print_exit()
