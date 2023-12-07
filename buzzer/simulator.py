import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame.mixer
import keyboard


def run_simulation():
    pygame.mixer.init()

    buzzer_sound_path = "buzzer/buzzer-sound.wav"
    buzzer_sound = pygame.mixer.Sound(buzzer_sound_path)

    try:
        print("Hold the 'B' button to buzz\nPress 'x' to return\n")
        while True:
            if keyboard.is_pressed('B'):
                buzzer_sound.play()
            elif keyboard.is_pressed('x'):
                break
            else:
                buzzer_sound.stop()
    except:
        pass
    finally:
        pygame.mixer.quit()
