import time
from datetime import datetime


def run_simulation(delay, stop_event):
    try:
        while True:
            if stop_event.is_set():
                return
            # todo print currrent time
            print("Time: ", datetime.now())
            time.sleep(delay)
    except KeyboardInterrupt:
        print("LCD simulation stopped by user.")
