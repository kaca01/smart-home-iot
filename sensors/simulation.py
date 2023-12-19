import os
import keyboard
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


def button_pressed_simulation(state):
    if state == 'x':
        print("The door is unlocked!")
    elif state == 'y':
        print("The door is locked!")
    else:
        print("Wrong input!")


def run_simulation(callback, publish_event, settings):
    door_locked = True
    try:
        print("Hold the 'D' button to unlock the door\n To exit press 'x'")
        while True:
            if keyboard.is_pressed('D'):
                if door_locked:
                    button_pressed_simulation('x')
                    door_locked = False
                    callback(False, publish_event, settings)
            elif keyboard.is_pressed('x'):
                return
            elif keyboard.is_pressed('ctrl'):
                return
            else:
                if not door_locked:
                    button_pressed_simulation('y')
                    door_locked = True
                    callback(True, publish_event, settings)

    except KeyboardInterrupt:
        print('Simulation stopped by user')
    except Exception as e:
        print(f'Error: {str(e)}')
