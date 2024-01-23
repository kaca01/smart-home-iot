import RPi.GPIO as GPIO
import time


def motion_detected(channel):
    print("You moved")


def no_motion(channel):
    print("You stopped moving")


def run_pir_loop(delay, callback, stop_event, publish_event, settings):
    pin = settings['pin']
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN)
    while True:
        GPIO.add_event_detect(pin, GPIO.RISING, callback=lambda _: callback(True, publish_event, settings))
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=no_motion)
        if stop_event.is_set():
            break
        time.sleep(delay) # Delay between readings
