import RPi.GPIO as GPIO
import time


def init_pin(buzzer_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)


def buzz(pitch, duration, buzzer_pin):
    period = 1.0 / pitch
    delay = period / 2
    cycles = int(duration * pitch)
    for i in range(cycles):
        GPIO.output(buzzer_pin, True)
        time.sleep(delay)
        GPIO.output(buzzer_pin, False)
        time.sleep(delay)


def run_actuator(pin):
    init_pin(pin)
    try:
        while True:
            pitch = 440
            duration = 0.1
            buzz(pitch, duration, pin)
            time.sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()