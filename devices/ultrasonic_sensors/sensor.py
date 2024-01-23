import time
import random
from time import sleep
import RPi.GPIO as GPIO

def get_distance(TRIG_PIN, ECHO_PIN):
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 1000

    iter = 0
    while GPIO.input(ECHO_PIN) == 0:
        if iter > max_iter:
            return None
        pulse_start_time = time.time()
        iter += 1

    iter = 0
    while GPIO.input(ECHO_PIN) == 1:
        if iter > max_iter:
            return None
        pulse_end_time = time.time()
        iter += 1

    pulse_duration = pulse_end_time - pulse_start_time
    distance = (pulse_duration * 34300)/2
    return distance


def is_locked(distance):
    if distance > 1:
        return False
    return True


def run_dus_loop(settings, callback, publish_event, event):
    GPIO.setmode(GPIO.BCM)

    TRIG_PIN = settings["pin"][0]
    ECHO_PIN = settings["pin"][1]

    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)

    try:
        while not event.is_set():
            distance = get_distance(TRIG_PIN, ECHO_PIN)
            callback(distance, publish_event, settings)
            
            if is_locked(distance):
                print(settings["name"] + ' says the door is locked!')
            else:
                print(settings["name"] + ' says the door is unlocked!')
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print('Measurement stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
