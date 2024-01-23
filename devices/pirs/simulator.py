import random
import time


def motion_detection_simulation(callback, stop, publish_event, pir_settings, settings):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        # print(rand)
        if rand > 0.8:
            print("You moved... ", pir_settings["name"])
            callback(True, publish_event, pir_settings, settings)
            # print(f"{device} says: you moved!")
        callback(False, publish_event, pir_settings, settings)
        time.sleep(1)
