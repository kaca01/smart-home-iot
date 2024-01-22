import time
from datetime import datetime


def run_simulation(delay, callback, stop_event, publish_event, settings):
    try:
        while True:
            if stop_event.is_set():
                return
            print("menjaj boju, ukljuci, iskljuci")
            # todo umesto da prosledis False prosledi sta treba
            callback(False, publish_event, settings)
            time.sleep(delay)
    except KeyboardInterrupt:
        print("BIR simulation stopped by user.")
