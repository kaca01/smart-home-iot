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
from menu_prints import print_lights_menu, print_main_menu, print_door_sensors_menu, print_exit, print_room_sensors_menu
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except ModuleNotFoundError:
    pass


# def handle_lights_menu():
#     while True:
#         print_lights_menu()
#         inp = str(input(""))
#         inp = inp.strip().lower()
#         if inp == "0":
#             break
#         elif inp == "1":
#             dl_settings = settings["DL"]
#             run_dl(dl_settings, '1')
#         elif inp == "2":
#             dl_settings = settings["DL"]
#             run_dl(dl_settings, '2')
#         else:
#             print("Invalid input!")
#     main()


# def handle_door_sensors_menu():
#     while True:
#         print_door_sensors_menu()
#         inp = str(input(""))
#         inp = inp.strip().lower()
#         if inp == "0":
#             break
#         elif inp == "1":
#             dus1_settings = settings["DUS1"]
#             thread = threading.Thread(target=run_dus1, args=(dus1_settings, stop_event_dus1))
#             thread.start()
#         elif inp == "2":
#             stop_event_dus1.set()
#         elif inp == "3":
#             dpir1_settings = settings["DPIR1"]
#             thread = threading.Thread(target=run_dpir1, args=(dpir1_settings, stop_event_dpir1))
#             thread.start()
#         elif inp == "4":
#             stop_event_dpir1.set()
#         else:
#             print("Invalid input!")
#     main()


# def handle_room_sensors_menu():
#     while True:
#         print_room_sensors_menu()
#         inp = str(input(""))
#         inp = inp.strip().lower()
#         if inp == "0":
#             break
#         elif inp == "1":
#             thread = threading.Thread(target=run_pir1, args=(settings["PIR1"], stop_event_pir1,))
#             thread.start()
#         elif inp == "2":
#             stop_event_pir1.set()
#         elif inp == "3":
#             thread = threading.Thread(target=run_pir2, args=(settings["PIR2"], stop_event_pir2,))
#             thread.start()
#         elif inp == "4":
#             stop_event_pir2.set()
#         elif inp == "5":
#             stop_event_dht1.clear()
#             thread = threading.Thread(target=run_dht1, args=(settings["DHT1"], stop_event_dht1))
#             thread.start()
#         elif inp == "6":
#             stop_event_dht1.set()
#         elif inp == "7":
#             stop_event_dht2.clear()
#             thread = threading.Thread(target=run_dht2, args=(settings["DHT2"], stop_event_dht2))
#             thread.start()
#         elif inp == "8":
#             stop_event_dht2.set()
#         else:
#             print("Invalid input!")

#     main()


# def main():
#     while True:
#         print_main_menu()
#         inp = str(input(""))
#         inp = inp.strip().lower()
#         if inp == "0":
#             for event in events:
#                 event.set()
#             print_exit()
#             exit()
#         elif inp == "1":
#             ds1_settings = settings["DS1"]
#             run_ds1(ds1_settings)
#         elif inp == "2":
#             handle_lights_menu()
#         elif inp == "3":
#             handle_door_sensors_menu()
#         elif inp == "4":
#             run_buzzer(settings['DB'])
#         elif inp == "5":
#             handle_room_sensors_menu()
#         elif inp == "6":
#             run_dms(settings["DMS"])
#         else:
#             print("Invalid input!")


if __name__ == "__main__":
        print('Starting app')
        settings = load_settings()
        threads = []

        # events
        stop_event_dht1 = threading.Event()
        stop_event_dht2 = threading.Event()
        stop_event_dht3 = threading.Event()
        stop_event_dht4 = threading.Event()
        stop_event_gdht = threading.Event()
        stop_event_pir1 = threading.Event()
        stop_event_pir2 = threading.Event()
        stop_event_pir3 = threading.Event()
        stop_event_pir4 = threading.Event()
        stop_event_ds1 = threading.Event()
        stop_event_ds2 = threading.Event()
        stop_event_dl = threading.Event()
        stop_event_dus1 = threading.Event()
        stop_event_dpir1 = threading.Event()
        stop_event_db = threading.Event()
        stop_event_dms = threading.Event()
        stop_event_rgb = threading.Event()
        stop_event_lcd = threading.Event()
        stop_event_dus2 = threading.Event()
        stop_event_bb = threading.Event()
        stop_event_b4sd = threading.Event()
        stop_event_bir = threading.Event()
        stop_event_gsg = threading.Event()

        events = []
        events += [stop_event_dht1, stop_event_dht2, stop_event_pir1, stop_event_pir2, stop_event_ds1, stop_event_dl,
                stop_event_dus1, stop_event_dpir1, stop_event_db, stop_event_dms, stop_event_rgb, stop_event_lcd, 
                stop_event_dus2, stop_event_ds2, stop_event_bb, stop_event_b4sd, stop_event_bir, stop_event_gsg]

        try:
                # PI1
                thread = threading.Thread(target=run_dht, args=(settings["DHT1"], stop_event_dht1))
                thread.start()

                thread = threading.Thread(target=run_dht, args=(settings["DHT2"], stop_event_dht2))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR1"], stop_event_pir1,))
                thread.start()

                thread = threading.Thread(target=run_pir, args=(settings["PIR2"], stop_event_pir2,))
                thread.start()

                thread = threading.Thread(target=run_dms, args=(settings["DMS"], stop_event_dms,))
                thread.start()

                thread = threading.Thread(target=run_dpir1, args=(settings["DPIR1"], stop_event_dpir1))
                thread.start()

                # thread = threading.Thread(target=run_buzzer, args=(settings["DB"], stop_event_db,))
                # thread.start()
                # threads.append(thread)

                thread = threading.Thread(target=run_dus1, args=(settings["DUS1"], stop_event_dus1,))
                thread.start()

                thread = threading.Thread(target=run_ds1, args=(settings["DS1"],))
                thread.start()

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
