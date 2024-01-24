try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    pass
import time
import threading


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


def play_sound(buzzer_pin, stop_event):
    while True:
        GPIO.output(buzzer_pin, True)
        time.sleep(1)
        GPIO.output(buzzer_pin, False)
        time.sleep(1)
        if stop_event.is_set():
            break


def button_pressed_pi(stop_event_audio, pin):
    with sound_lock:
        print('yees')
        stop_event_audio.clear()
        audio_thread = threading.Thread(target=play_sound, args=(pin, stop_event_audio,))
        audio_thread.start()


def button_released_pi(stop_event_audio):
    with sound_lock:
        print('no')
        stop_event_audio.set()

sound_lock = threading.Lock()

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