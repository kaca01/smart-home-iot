# if pressed the door is opened
# else closed

# import RPi.GPIO as GPIO


def button_pressed_simulation(state):
    if state == 'x':
        print("The door is unlocked!")
    elif state == 'y':
        print("The door is locked!")
    else:
        print("Wrong input!")


# TODO: this code should be checked on pi
# def button_pressed(event):
#     if GPIO.input(PORT_BUTTON):
#         print("The door is locked!")
#     else:
#         print("The door is unlocked!")


if __name__ == '__main__':

    try:
        # simulation
        print("Press x to unlock the door\nPress y to lock the door\n")
        while True:
            inp = str(input())
            button_pressed_simulation(inp.strip().lower())

        # real-time
        # PORT_BUTTON = 17
        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(PORT_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        # TODO: this also
        # GPIO.add_event_detect(PORT_BUTTON, GPIO.BOTH, callback=button_pressed, bouncetime = 100)
        # input("Press any key to exit...")
    except KeyboardInterrupt:
        print('Simulation stopped by user')
        # GPIO.cleanup()
    except Exception as e:
        print(f'Error: {str(e)}')
        # GPIO.cleanup()


