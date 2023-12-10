from buzzer.simulator import run_simulation
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import threading
import pygame


sound_lock = threading.Lock()

def sound_play(stop_event_audio):
    while True:
        try:
            pygame.mixer.init()
            sound = pygame.mixer.Sound("./buzzer/buzzer-sound.wav")
            sound.play()
            if stop_event_audio.is_set():
                break
        except Exception as e:
            break


def button_pressed(stop_event_audio):
    with sound_lock:
        print('radiii')
        stop_event_audio.clear()
        audio_thread = threading.Thread(target=sound_play, args=(stop_event_audio,))
        audio_thread.start()


def button_released(stop_event_audio):
    with sound_lock:
        print('ne cuje se vise')
        stop_event_audio.set()


def run_buzzer(settings, stop_event):
    stop_event_audio = threading.Event()
    if settings['simulated']:
        print("Buzzer sumilator")
        run_simulation(2, button_pressed, button_released, stop_event, stop_event_audio)
    else:
        from buzzer.actuator import run_actuator
        print("Buzzer running")
        run_actuator(settings['pin'])
