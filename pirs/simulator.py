import random
import time


def motion_detection_simulation(stop):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        if rand > 0.8:
            print(f"You moved! {rand}")
            # e.set()
        time.sleep(1)
