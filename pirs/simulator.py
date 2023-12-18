import random
import time


def motion_detection_simulation(callback, stop, publish_event, pir_settings):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        # print(rand)
        if rand > 0.8:
            callback(True, publish_event, pir_settings)
            # print(f"{device} says: you moved!")
        time.sleep(1)
