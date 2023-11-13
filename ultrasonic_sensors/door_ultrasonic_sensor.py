import time
import random
from time import sleep
from ultrasonic_sensors.simulation import run_simulation


def get_distance():
    GPIO.output(TRIG_PIN, False)
    time.sleep(0.2)
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    pulse_start_time = time.time()
    pulse_end_time = time.time()

    max_iter = 100

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


def run_dus1(settings, event):
    if settings["simulated"]:
        run_simulation(event)
    else:
        # real-time
        import RPi.GPIO as GPIO
        GPIO.setmode(GPIO.BCM)

        TRIG_PIN = settings["pin"][0]
        ECHO_PIN = settings["pin"][1]

        GPIO.setup(TRIG_PIN, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)

        try:
            while True:
                distance = get_distance()
                if is_locked(distance):
                    print('The door is locked!')
                else:
                    print('The door is unlocked!')
                time.sleep(1)
        except KeyboardInterrupt:
            # GPIO.cleanup()
            print('Measurement stopped by user')
        except Exception as e:
            print(f'Error: {str(e)}')
