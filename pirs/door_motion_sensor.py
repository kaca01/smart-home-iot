import random
import threading
import time
import pirs.simulator
from pirs.simulator import motion_detection_simulation


# def motion_detection_simulation(e, stop):
#     while not stop.is_set():
#         rand = round(random.uniform(0, 1), 2)
#         if rand > 0.8:
#             # print you moved can also be here
#             e.set()
#         time.sleep(1)


def motion_detected(channel):
    print("You moved")


def no_motion(channel):
    print("You stopped moving")


def run_dpir1(settings, stop_event):
    # simulation
    if settings["simulated"]:
        # event = threading.Event()
        # # stop_event = threading.Event()
        # thread = threading.Thread(target=motion_detection_simulation, args=(event, stop_event))
        # thread.start()

        try:
            motion_detection_simulation(stop_event)
            # while True:
            #     event.wait()  # if something is happening after event is triggered (waiting for event)
            #     # print("You moved")
            #     event.clear()
        except KeyboardInterrupt:
            print("Simulation stopped by user")
            stop_event.set()
            # thread.join()
        except Exception as e:
            print(f'Error: {str(e)}')
            stop_event.set()
            # thread.join()

    else:
        # TODO: thread should be here also
        import RPi.GPIO as GPIO
        PIR_PIN = settings["pin"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIR_PIN, GPIO.IN)
        GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
        GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=no_motion)
        input("Press any key to exit...")
