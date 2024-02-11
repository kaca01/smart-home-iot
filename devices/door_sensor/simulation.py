import os
# import keyboard
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import time
import random


def button_pressed_simulation(state):
    if state == 'x':
        print("The door is unlocked!")
    elif state == 'y':
        print("The door is locked!")
    else:
        print("Wrong input!")


def generate_value(delay, previous_value=False):
    while True:
        time.sleep(delay)
        new_value = random.randint(1, 2) == 2
        if new_value == previous_value:
            continue
        else:
            previous_value = new_value
            yield new_value


def run_simulation(callback, publish_event, settings, stop_event):
    door_locked = True
    try:
        # print("Hold the 'D' button to unlock the door\n To exit press 'x'")
        # while True:
        #     if keyboard.is_pressed('D'):
        #         if door_locked:
        #             button_pressed_simulation('x')
        #             door_locked = False
        #             callback(False, publish_event, settings)
        #     elif keyboard.is_pressed('x'):
        #         return
        #     elif keyboard.is_pressed('ctrl'):
        #         return
        #     else:
        #         if not door_locked:
        #             button_pressed_simulation('y')
        #             door_locked = True
        #             callback(True, publish_event, settings)
        for pressed in generate_value(2):
            if pressed:
                callback(True, publish_event, settings)
            else:
                callback(False, publish_event, settings)
            if stop_event.is_set():
                break

    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
