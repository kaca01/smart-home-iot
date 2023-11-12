import random
import time


def motion_detection_simulation(stop):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        print(rand)
        if rand > 0.8:
            print(f"You moved! {rand}")
        time.sleep(1)
