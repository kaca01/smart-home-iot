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


def run_pir_loop(pir, delay, callback, stop_event, publish_event, settings):
    while True:
        GPIO.add_event_detect(pir.pin, GPIO.RISING, callback=lambda _: callback(True, publish_event, settings)) # todo proveri da li radi
        GPIO.add_event_detect(pir.pin, GPIO.FALLING, callback=no_motion)
        if stop_event.is_set():
            break
        time.sleep(delay) # Delay between readings
