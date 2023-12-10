import time
import random


def generate_value(delay):
    helper = False
    while True:
        time.sleep(delay)
        is_pressed = random.randint(0, 1) == 1
        if is_pressed == helper : 
            continue
        else:
            helper = is_pressed
            yield is_pressed


def run_simulation(delay, callback_pressed, callback_released, stop_event, stop_event_audio):
    for pressed in generate_value(delay):
        if pressed:
            callback_pressed(stop_event_audio)
        else:
            callback_released(stop_event_audio)
        if stop_event.is_set():
            stop_event_audio.set()
            break
