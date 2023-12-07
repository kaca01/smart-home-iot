import RPi.GPIO as GPIO
import time


class PIR(object):
    def __init__(self, pin):
        self.pin = pin


    def set_sensor(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)


def motion_detected(channel):
    print("You moved")


def no_motion(channel):
    print("You stopped moving")


# input("Press any key to exit...")

def run_pir_loop(pir, delay, stop_event):
    while True:
        GPIO.add_event_detect(pir.pin, GPIO.RISING, callback=motion_detected)
        GPIO.add_event_detect(pir.pin, GPIO.FALLING, callback=no_motion)
        if stop_event.is_set():
            break
        time.sleep(delay) # Delay between readings