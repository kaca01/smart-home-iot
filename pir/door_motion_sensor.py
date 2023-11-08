import random
import threading
import time


def motion_detected_simulation(e, stop):
    while not stop.is_set():
        rand = round(random.uniform(0, 1), 2)
        print("Rand", rand)
        if rand > 0.5:
            e.set()
        time.sleep(1)


if __name__ == '__main__':
    event = threading.Event()
    stop_event = threading.Event()
    thread = threading.Thread(target=motion_detected_simulation, args=(event, stop_event,))
    thread.start()

    try:
        while True:
            event.wait()
            print("You moved")
            event.clear()
    except KeyboardInterrupt:
        print("Simulation stopped by user")
        stop_event.set()
        thread.join()
    except Exception as e:
        print(f'Error: {str(e)}')
        thread.join()
