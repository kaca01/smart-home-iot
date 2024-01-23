import random
import time


def motion_detection_simulation(callback, stop, publish_event, pir_settings, settings, thread):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        # print(rand)
        if rand > 0.8:
            print("You moved... ", pir_settings["name"])
            ret = callback(True, publish_event, pir_settings, settings, thread)
            # print(f"{device} says: you moved!")
            if ret is not None:
                thread = ret
        else:
            callback(False, publish_event, pir_settings, settings, thread)
        time.sleep(1)
